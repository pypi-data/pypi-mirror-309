from bananopie import RPC, get_public_key_from_address, get_address_from_public_key
from .constants import *
from .util import decode_domain_name

class Account:
  def __init__(self, rpc: RPC, address: str):
    self.rpc = rpc
    self.address = address
  def get_open_and_frontier(self):
    account_info = self.rpc.get_account_info(self.address)
    return [account_info["open_block"], account_info["confirmation_height_frontier"] or account_info["frontier"]]
  def get_history_from_open(self, head: str, count: int):
    return self.rpc.get_account_history(self.address, count=count, head=head, raw=True, reverse=True)

class TldAccount(Account):
  def __init__(self, rpc: RPC, address: str):
    super().__init__(rpc, address)
    self.all_issued = []
  def get_specific(self, name: str):
    open_hash, frontier_hash = self.get_open_and_frontier()
    head_hash = open_hash
    while True:
      history = self.get_history_from_open(head_hash, 100)["history"]
      for block in history:
        if len(block["amount"]) == 27:
          if block["subtype"] == "send" and block["amount"].startswith(TRANS_START) and (block["amount"][len(TRANS_START)] == "1" or block["amount"] == TRANS_MAX):
            decoded_name = decode_domain_name(get_public_key_from_address(block["representative"]))
            if decoded_name == name:
              return {
                "tld": self.address,
                "name": name,
                "history": [
                  {
                    "type": "transfer",
                    "block": block,
                    "to": get_address_from_public_key(block["link"]),
                  },
                ],
              }
        if (block["representative"] == FREEZE_REP and block["subtype"] == "change") or block["hash"] == frontier_hash:
          return
      head_hash = history[len(history) - 1].hash;
  def get_all_issued():
    open_hash, frontier_hash = self.get_open_and_frontier()
    head_hash = open_hash
    issued = {}
    while True:
      history = self.get_history_from_open(head_hash, 100)["history"]
      for block in history:
        if len(block["amount"]) == 27:
          if block["subtype"] == "send" and block["amount"].startswith(TRANS_START) and (block["amount"][len(TRANS_START)] == "1" or block["amount"] == TRANS_MAX):
            decoded_name = decode_domain_name(get_public_key_from_address(block["representative"]))
            if not issued[decoded_name]:
              issued[decoded_name] = {
                "tld": self.address,
                "name": name,
                "history": [
                  {
                    "type": "transfer",
                    "block": block,
                    "to": get_address_from_public_key(block.link),
                  },
                ],
              }
        if (block["representative"] == FREEZE_REP and block["subtype"] == "change") or block["hash"] == frontier_hash:
          self.all_issued = issued.values()
          return self.all_issued
      head_hash = history[len(history) - 1].hash;

class DomainAccount(Account):
  def __init__(self, rpc: RPC, address: str, domain = None):
    super().__init__(rpc, address)
    self.domain = domain
  def crawl(self):
    try:
      open_hash, frontier_hash = self.get_open_and_frontier()
    except Exception:
      return self.domain
    head_hash = open_hash
    while True:
      history = self.get_history_from_open(head_hash, 100)["history"]
      for block in history:
        if "amount" not in block:
          amount = "0"
        else:
          amount = block["amount"]
        if block["height"] == "1":
          last_block = self.domain["history"][len(self.domain["history"]) - 1]
          if last_block:
            if block["link"] != last_block["block"]["hash"]:
              self.domain.burned = true
              return self.domain
          self.domain["history"].append({
            "type": "receive",
            "block": block,
          });
        elif len(amount) == 27:
          if block["subtype"] == "send" and amount.startswith(TRANS_START) and (amount[len(TRANS_START)] == "1" or amount == TRANS_MAX):
            decoded_name = decode_domain_name(get_public_key_from_address(block["representative"]))
            if decoded_name == self.domain:
              self.domain["resolved_address"] = None
              self.domain["metadata_hash"] = None
              self.domain["history"].append({
                "type": "transfer",
                "block": block,
                "to": get_address_from_public_key(block["link"]),
              })
              return self.domain
        elif block["subtype"] == "change" and block["representative"] == FREEZE_REP:
          self.domain["history"].append({
            "type": "freeze",
            "block": block,
          })
          return self.domain
        elif block["subtype"] == "change":
          self.domain["metadata_hash"] = get_public_key_from_address(block["representative"])
          self.domain["history"].append({
            "type": "metadata",
            "block": block,
            "metadata_hash": self.domain["metadata_hash"],
          })
        elif block["subtype"] == "send" and amount == "4224":
          self.domain["resolved_address"] = get_address_from_public_key(block["link"])
          self.domain["history"].append({
            "type": "resolver",
            "block": block,
            "resolved_address": self.domain["resolved_address"],
          })
        if block["hash"] == frontier_hash:
          return self.domain
      head_hash = history[len(history) - 1].hash;

class Resolver:
  def __init__(self, rpc: RPC, tld_mapping):
    self.rpc = rpc
    self.tld_mapping = tld_mapping
  def resolve(self, domain_name: str, tld: str):
    domain_name = domain_name.lower()
    if not self.tld_mapping[tld]:
      raise Exception("No TLD Account found for that TLD")
    tld_account = TldAccount(self.rpc, self.tld_mapping[tld])
    domain = tld_account.get_specific(domain_name)
    if not domain:
      return domain
    while True:
      current_domain_account = domain["history"][len(domain["history"]) - 1]["to"]
      domain_account = DomainAccount(self.rpc, current_domain_account, domain)
      old_l = len(domain["history"])
      domain = domain_account.crawl()
      if domain["history"][len(domain["history"]) - 1]["type"] != "transfer" or domain["burned"] or old_l == len(domain["history"]):
        break
    return domain
  def resolve_backwards_ish(self, domain_account_address: str, tld: str):
    open_hash = self.rpc.get_account_info(domain_account_address)["open_block"]
    transfer_hash = self.rpc.get_block_info(open_hash)["contents"]["link"]
    transfer_block = self.rpc.get_block_info(transfer_hash)
    domain_name = decode_domain_name(get_public_key_from_address(transfer_block["contents"]["representative"]))
    domain = self.resolve(domain_name, tld)
    if domain:
      #python sucks
      last_transfer = next((block for block in list(reversed(domain["history"])) if block["type"] == "transfer"), None) 
      if last_transfer["to"] == domain_account_address:
        return domain

