"""Helpers for the local test lab: put the seeded database in a known state and read it back, so a run can be checked against the real records.

  python lab.py reset            delete every match, conversation and message (the 14 seeded users stay)
  python lab.py prime EMAIL ...  make each named seeded user like the lab account first, so the account's own like turns into a match
  python lab.py reply NAME       add one reply from the named seeded user to the conversation the lab account started with them
  python lab.py status           counts of matches by status and messages, and the matches of the lab account

Everything goes through `docker compose exec api bin/rails runner` against the Rails API container of this repo (the compose files in the repo root and
automation/compose.emulator.yml), so it only ever touches the local development database. Set API_PORT when 3000 is taken.
"""
import json
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAB_EMAIL = os.environ.get("CHATDATERS_EMAIL", "user1@gmail.com")
COMPOSE = ["docker", "compose", "-f", "docker-compose.yml", "-f", "automation/compose.emulator.yml"]


def rails(code, timeout=120):
    out = subprocess.run(COMPOSE + ["exec", "-T", "api", "bin/rails", "runner", code], cwd=REPO, capture_output=True, text=True, timeout=timeout)
    if out.returncode != 0:
        raise RuntimeError("rails runner failed: " + (out.stderr or out.stdout).strip()[-400:])
    return out.stdout.strip()


def reset():
    rails("Message.delete_all; Conversation.delete_all; Match.delete_all; puts 'reset'")


def prime(emails):
    code = ("me = User.find_by!(email: %s); %s.each { |e| u = User.find_by!(email: e); ids = [me.id, u.id].sort; "
            "Match.find_or_create_by!(user_ids: ids) { |m| m.user_initiated = u.id; m.user_received = me.id; m.status = 'pending' } }; puts 'primed'") % (json.dumps(LAB_EMAIL), json.dumps(emails))
    rails(code)


def reply(first_name):
    code = ("me = User.find_by!(email: %s); other = User.where(first_name: %s).where.not(id: me.id).first!; "
            "conv = Conversation.where('? = ANY(user_ids)', me.id).detect { |c| c.user_ids.include?(other.id) }; raise 'no conversation' unless conv; "
            "Message.create!(sender_id: other.id, receiver_id: me.id, content: 'Hi, doing well, thanks for asking.', conversation_id: conv.id); puts 'replied'") % (json.dumps(LAB_EMAIL), json.dumps(first_name))
    rails(code)


def status():
    code = ("me = User.find_by!(email: %s); puts({matches: Match.group(:status).count, messages: Message.count, "
            "mine: Match.where('? = ANY(user_ids)', me.id).map { |m| [User.find((m.user_ids - [me.id]).first).first_name, m.status] }}.to_json)") % json.dumps(LAB_EMAIL)
    return json.loads(rails(code).splitlines()[-1])


def main(argv):
    cmd = argv[0] if argv else ""
    if cmd == "reset":
        reset()
    elif cmd == "prime" and len(argv) > 1:
        prime(argv[1:])
    elif cmd == "reply" and len(argv) == 2:
        reply(argv[1])
    elif cmd == "status":
        print(json.dumps(status(), indent=2))
        return 0
    else:
        print(__doc__)
        return 2
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
