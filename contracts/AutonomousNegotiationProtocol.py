# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from genlayer import *

EXPECTED = "[EXPECTED]"
LLM_ERROR = "[LLM_ERROR]"


def _now() -> int:
    return int(datetime.fromisoformat(gl.message_raw["datetime"]).timestamp())


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


@allow_storage
@dataclass
class Policy:
    owner: Address
    party_a: Address
    party_b: Address
    objective_a: str
    objective_b: str
    asset: str
    max_price: u256
    min_quality: u256
    deadline: u256
    max_rounds: u256


@allow_storage
@dataclass
class Session:
    policy_id: str
    state: str
    current_round: u256
    current_proposal: str
    proposal_root: str


@allow_storage
@dataclass
class Proposal:
    session_id: str
    proposer: Address
    terms_hash: str
    asset: str
    price: u256
    quality: u256
    conditions: str
    parent: str
    round: u256
    valid: bool


@allow_storage
@dataclass
class Certificate:
    certificate_id: str
    terms_hash: str
    proof_root: str
    fairness_score: u256
    alignment_score: u256
    finalized_at: u256
    consumed: bool


class AutonomousNegotiationProtocol(gl.Contract):
    policies: TreeMap[str, Policy]
    sessions: TreeMap[str, Session]
    proposals: TreeMap[str, Proposal]
    commitments: TreeMap[str, bool]
    proofs: TreeMap[str, str]
    certificates: TreeMap[str, Certificate]

    def __init__(self) -> None:
        pass

    @gl.public.write
    def create_policy(self, policy_id: str, party_a: Address, party_b: Address,
                      objective_a: str, objective_b: str, asset: str,
                      max_price: u256, min_quality: u256,
                      deadline: u256, max_rounds: u256) -> None:
        if policy_id == "" or policy_id in self.policies:
            raise gl.UserError(f"{EXPECTED} invalid policy")
        if party_a == party_b or objective_a == "" or objective_b == "" or asset == "":
            raise gl.UserError(f"{EXPECTED} invalid participants")
        if max_price == 0 or min_quality > 100 or deadline <= _now() or max_rounds == 0 or max_rounds > 20:
            raise gl.UserError(f"{EXPECTED} invalid bounds")
        self.policies[policy_id] = Policy(gl.message.sender_address, party_a, party_b,
            objective_a, objective_b, asset, max_price, min_quality, deadline, max_rounds)

    @gl.public.write
    def open_session(self, session_id: str, policy_id: str) -> None:
        if session_id == "" or session_id in self.sessions or policy_id not in self.policies:
            raise gl.UserError(f"{EXPECTED} invalid session")
        policy = self.policies[policy_id]
        if gl.message.sender_address != policy.owner or policy.deadline <= _now():
            raise gl.UserError(f"{EXPECTED} unauthorized or expired")
        self.sessions[session_id] = Session(policy_id, "OPEN", 0, "", _hash(session_id + "|" + policy_id))

    @gl.public.write
    def submit_proposal(self, proposal_id: str, session_id: str, terms_hash: str,
                        asset: str, price: u256, quality: u256,
                        conditions: str, parent: str) -> None:
        if proposal_id == "" or proposal_id in self.proposals or session_id not in self.sessions:
            raise gl.UserError(f"{EXPECTED} invalid proposal")
        session = self.sessions[session_id]
        policy = self.policies[session.policy_id]
        sender = gl.message.sender_address
        if sender != policy.party_a and sender != policy.party_b:
            raise gl.UserError(f"{EXPECTED} UNAUTHORIZED_NEGOTIATOR")
        if policy.deadline <= _now() or session.current_round >= policy.max_rounds or session.state in ("FINALIZED", "EXECUTED", "INVALID"):
            raise gl.UserError(f"{EXPECTED} negotiation closed")
        if (session.current_round == 0 and parent not in ("", "ROOT")) or (session.current_round > 0 and parent != session.current_proposal):
            raise gl.UserError(f"{EXPECTED} stale proposal parent")
        valid = asset == policy.asset and price <= policy.max_price and quality >= policy.min_quality
        round_number = session.current_round + 1
        self.proposals[proposal_id] = Proposal(session_id, sender, terms_hash, asset,
            price, quality, conditions, parent, round_number, valid)
        session.current_round = round_number
        session.current_proposal = proposal_id
        session.proposal_root = _hash(session.proposal_root + "|" + proposal_id + "|" + terms_hash)
        session.state = "PROPOSAL_SUBMITTED" if valid else "CONSTRAINT_FAILURE"
        self.sessions[session_id] = session

    @gl.public.write
    def commit(self, session_id: str, proposal_id: str, terms_hash: str) -> None:
        session = self.sessions[session_id]
        proposal = self.proposals[proposal_id]
        policy = self.policies[session.policy_id]
        sender = gl.message.sender_address
        if sender != policy.party_a and sender != policy.party_b:
            raise gl.UserError(f"{EXPECTED} UNAUTHORIZED_NEGOTIATOR")
        if session.state not in ("PROPOSAL_SUBMITTED", "FINAL_REVIEW"):
            raise gl.UserError(f"{EXPECTED} terminal session")
        if session.current_proposal != proposal_id or proposal.session_id != session_id or not proposal.valid:
            raise gl.UserError(f"{EXPECTED} inactive proposal")
        if terms_hash != proposal.terms_hash:
            raise gl.UserError(f"{EXPECTED} TERM_MISMATCH")
        self.commitments[proposal_id + "|" + str(sender)] = True
        session.state = "FINAL_REVIEW"
        self.sessions[session_id] = session

    @gl.public.write
    def finalize(self, session_id: str, proposal_id: str) -> None:
        session = self.sessions[session_id]
        if session.state not in ("FINAL_REVIEW", "PROPOSAL_SUBMITTED"):
            raise gl.UserError(f"{EXPECTED} session not finalizable")
        if session_id in self.certificates:
            raise gl.UserError(f"{EXPECTED} CERTIFICATE_EXISTS")
        proposal = self.proposals[proposal_id]
        policy = self.policies[session.policy_id]
        identity = proposal.proposer == policy.party_a or proposal.proposer == policy.party_b
        constraints = proposal.valid
        commitment = self.commitments.get(proposal_id + "|" + str(policy.party_a), False) and self.commitments.get(proposal_id + "|" + str(policy.party_b), False)
        freshness = session.current_proposal == proposal_id and policy.deadline > _now()
        prompt = ("Assess a bounded two-party negotiation. Return JSON only: alignment_score and fairness_score integers 0-100, improvement boolean. "
            "Fairness rejects exploitation. Alignment requires meaningful value for both objectives. A reasonable first offer counts as improvement. "
            f"A objective: {policy.objective_a}. B objective: {policy.objective_b}. Round: {proposal.round}. "
            f"Price: {proposal.price}. Quality: {proposal.quality}. Conditions: {proposal.conditions}.")

        def assess() -> dict:
            result = gl.nondet.exec_prompt(prompt, response_format="json")
            if not isinstance(result, dict):
                raise gl.vm.UserError(f"{LLM_ERROR} non-object")
            try:
                alignment = max(0, min(100, int(result.get("alignment_score", 0))))
                fairness = max(0, min(100, int(result.get("fairness_score", 0))))
            except Exception:
                raise gl.vm.UserError(f"{LLM_ERROR} invalid scores")
            return {"alignment": alignment >= 70, "fairness": fairness >= 70,
                "improvement": result.get("improvement") is True,
                "alignment_bucket": alignment // 10, "fairness_bucket": fairness // 10,
                "alignment_score": alignment, "fairness_score": fairness}

        def validate(leader: gl.vm.Result) -> bool:
            if not isinstance(leader, gl.vm.Return):
                return False
            other = assess()
            stable = all(leader.calldata.get(k) == other[k] for k in ("alignment", "fairness", "improvement"))
            close = abs(leader.calldata.get("alignment_bucket", -100) - other["alignment_bucket"]) <= 1 and abs(leader.calldata.get("fairness_bucket", -100) - other["fairness_bucket"]) <= 1
            return stable and close

        semantic = gl.vm.run_nondet_unsafe(assess, validate)
        vector = {"identity": identity, "constraints": constraints,
            "alignment": semantic["alignment"], "fairness": semantic["fairness"],
            "improvement": semantic["improvement"], "commitment": commitment,
            "freshness": freshness}
        vector_json = json.dumps(vector, sort_keys=True, separators=(",", ":"))
        proof_root = _hash(session.proposal_root + "|" + proposal.terms_hash + "|" + vector_json)
        approved = all(vector.values())
        self.proofs[session_id] = json.dumps({"vector": vector, "proof_root": proof_root, "approved": approved}, sort_keys=True)
        if not approved:
            session.state = "INVALID"
        else:
            certificate_id = _hash(session_id + "|" + proposal_id + "|" + proof_root)
            self.certificates[session_id] = Certificate(certificate_id, proposal.terms_hash,
                proof_root, semantic["fairness_score"], semantic["alignment_score"], _now(), False)
            session.state = "FINALIZED"
        self.sessions[session_id] = session

    @gl.public.write
    def execute(self, session_id: str, terms_hash: str) -> None:
        session = self.sessions[session_id]
        if session.state != "FINALIZED":
            raise gl.UserError(f"{EXPECTED} session not executable")
        certificate = self.certificates[session_id]
        if certificate.consumed:
            raise gl.UserError(f"{EXPECTED} ALREADY_EXECUTED")
        if terms_hash != certificate.terms_hash:
            raise gl.UserError(f"{EXPECTED} TERM_MISMATCH")
        certificate.consumed = True
        self.certificates[session_id] = certificate
        session.state = "EXECUTED"
        self.sessions[session_id] = session

    @gl.public.view
    def get_session(self, session_id: str) -> dict:
        item = self.sessions[session_id]
        return {"policy_id": item.policy_id, "state": item.state, "current_round": item.current_round, "current_proposal": item.current_proposal, "proposal_root": item.proposal_root}

    @gl.public.view
    def get_proof(self, session_id: str) -> str:
        return self.proofs[session_id]

    @gl.public.view
    def get_certificate(self, session_id: str) -> dict:
        item = self.certificates[session_id]
        return {"certificate_id": item.certificate_id, "terms_hash": item.terms_hash,
            "proof_root": item.proof_root, "fairness_score": item.fairness_score,
            "alignment_score": item.alignment_score, "finalized_at": item.finalized_at,
            "consumed": item.consumed}
