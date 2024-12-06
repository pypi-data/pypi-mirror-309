from __future__ import annotations

import abc
import json
import random
from dataclasses import dataclass
from enum import Enum, StrEnum
from typing import Generic, TypeVar, Any

from pydantic import BaseModel, ConfigDict, Field, field_serializer
from pydantic.alias_generators import to_camel

from SolSystem.Models.Common.Configuration import Configuration
from SolSystem.Models.Common.DataTypes import UInt32
from SolSystem.Models.Common.Response import RpcVersion, Response, WsResponse


class RPCMethodName(StrEnum):
	ACCOUNT_INFO                       = "getAccountInfo"
	BALANCE                            = "getBalance"
	BLOCK                              = "getBlock"
	BLOCK_COMMITMENT                   = "getBlockCommitment"
	BLOCK_HEIGHT                       = "getBlockHeight"
	BLOCK_PRODUCTION                   = "getBlockProduction"
	BLOCK_TIME                         = "getBlockTime"
	BLOCKS                             = "getBlocks"
	BLOCKS_WITH_LIMIT                  = "getBlocksWithLimit"
	CLUSTER_NODES                      = "getClusterNodes"
	EPOCH_INFO                         = "getEpochInfo"
	EPOCH_SCHEDULE                     = "getEpochSchedule"
	FEE_FOR_MESSAGE                    = "getFeeForMessage"
	FIRST_AVAILABLE_BLOCK              = "getFirstAvailableBlock"
	GENESIS_HASH                       = "getGenesisHash"
	HEALTH                             = "getHealth"
	HIGHEST_SNAPSHOT_SLOT              = "getHighestSnapshotSlot"
	IDENTITY                           = "getIdentity"
	INFLATION_GOVERNOR                 = "getInflationGovernor"
	INFLATION_RATE                     = "getInflationRate"
	INFLATION_REWARD                   = "getInflationReward"
	LARGEST_ACCOUNTS                   = "getLargestAccounts"
	LATEST_BLOCKHASH                   = "getLatestBlockhash"
	LEADER_SCHEDULE                    = "getLeaderSchedule"
	MAX_RETRANSMIT_SLOT                = "getMaxRetransmitSlot"
	MAX_SHRED_INSERT_SLOT              = "getMaxShredInsertSlot"
	MINIMUM_BALANCE_FOR_RENT_EXEMPTION = "getMinimumBalanceForRentExemption"
	MULTIPLE_ACCOUNTS                  = "getMultipleAccounts"
	PROGRAM_ACCOUNTS                   = "getProgramAccounts"
	RECENT_PERFORMANCE_SAMPLES         = "getRecentPerformanceSamples"
	RECENT_PRIORITIZATION_FEES         = "getRecentPrioritizationFees"
	SIGNATURE_STATUSES                 = "getSignatureStatuses"
	SIGNATURES_FOR_ADDRESS             = "getSignaturesForAddress"
	SLOT                               = "getSlot"
	SLOT_LEADER                        = "getSlotLeader"
	SLOT_LEADERS                       = "getSlotLeaders"
	STAKE_ACTIVATION                   = "getStakeActivation"
	STAKE_MINIMUM_DELEGATION           = "getStakeMinimumDelegation"
	SUPPLY                             = "getSupply"
	TOKEN_ACCOUNT_BALANCE              = "getTokenAccountBalance"
	TOKEN_ACCOUNTS_BY_DELEGATE         = "getTokenAccountsByDelegate"
	TOKEN_ACCOUNTS_BY_OWNER            = "getTokenAccountsByOwner"
	TOKEN_LARGEST_ACCOUNTS             = "getTokenLargestAccounts"
	TOKEN_SUPPLY                       = "getTokenSupply"
	TRANSACTION                        = "getTransaction"
	TRANSACTION_COUNT                  = "getTransactionCount"
	VERSION                            = "getVersion"
	VOTE_ACCOUNTS                      = "getVoteAccounts"
	IS_BLOCKHASH_VALID                 = "isBlockhashValid"
	MINIMUM_LEDGER_SLOT                = "minimumLedgerSlot"
	REQUEST_AIRDROP                    = "requestAirdrop"
	SEND_TRANSACTION                   = "sendTransaction"
	SIMULATE_TRANSACTION               = "simulateTransaction"



class DasMethodName(StrEnum): 
	ASSET = "getAsset"
	GET_TOKEN_ACCOUNTS = "getTokenAccounts"



@dataclass(eq = True, frozen = True)
class WsMethodNameMixin:
	subscribe: str
	unsubscribe: str



class WsMethodName(WsMethodNameMixin, Enum): 
	ACCOUNT            = "accountSubscribe",      "accountUnsubscribe"
	BLOCK              = "blockSubscribe",        "blockUnsubscribe"
	LOGS               = "logsSubscribe",         "logsUnsubscribe"
	PROGRAM            = "programSubscribe",      "programUnsubscribe"
	ROOT               = "rootSubscribe",         "rootUnsubscribe"
	SIGNATURE          = "signatureSubscribe",    "signatureUnsubscribe"
	SLOT               = "slotSubscribe",         "slotUnsubscribe"
	SLOTS_UPDATES      = "slotsUpdatesSubscribe", "slotsUpdatesUnsubscribe"
	VOTE               = "voteSubscribe",         "voteUnsubscribe"
	HELIUS_TRANSACTION = "transactionSubscribe",  "transactionUnsubscribe"



MethodAPICost = {
	RPCMethodName.ACCOUNT_INFO: 1,
	RPCMethodName.BALANCE: 1,
	RPCMethodName.BLOCK: 10,
	RPCMethodName.BLOCK_COMMITMENT: 1,
	RPCMethodName.BLOCK_HEIGHT: 1,
	RPCMethodName.BLOCK_PRODUCTION: 1,
	RPCMethodName.BLOCK_TIME: 10,
	RPCMethodName.BLOCKS: 10,
	RPCMethodName.BLOCKS_WITH_LIMIT: 1,
	RPCMethodName.CLUSTER_NODES: 1,
	RPCMethodName.EPOCH_INFO: 1,
	RPCMethodName.EPOCH_SCHEDULE: 1,
	RPCMethodName.FEE_FOR_MESSAGE: 1,
	RPCMethodName.FIRST_AVAILABLE_BLOCK: 1,
	RPCMethodName.GENESIS_HASH: 1,
	RPCMethodName.HEALTH: 1,
	RPCMethodName.HIGHEST_SNAPSHOT_SLOT: 1,
	RPCMethodName.IDENTITY: 1,
	RPCMethodName.INFLATION_GOVERNOR: 1,
	RPCMethodName.INFLATION_RATE: 1,
	RPCMethodName.INFLATION_REWARD: 10,
	RPCMethodName.LARGEST_ACCOUNTS: 1,
	RPCMethodName.LATEST_BLOCKHASH: 1,
	RPCMethodName.LEADER_SCHEDULE: 1,
	RPCMethodName.MAX_RETRANSMIT_SLOT: 1,
	RPCMethodName.MAX_SHRED_INSERT_SLOT: 1,
	RPCMethodName.MINIMUM_BALANCE_FOR_RENT_EXEMPTION: 1,
	RPCMethodName.MULTIPLE_ACCOUNTS: 1,
	RPCMethodName.PROGRAM_ACCOUNTS: 1,
	RPCMethodName.RECENT_PERFORMANCE_SAMPLES: 1,
	RPCMethodName.RECENT_PRIORITIZATION_FEES: 1,
	RPCMethodName.SIGNATURE_STATUSES: 1,
	RPCMethodName.SIGNATURES_FOR_ADDRESS: 10,
	RPCMethodName.SLOT: 1,
	RPCMethodName.SLOT_LEADER: 1,
	RPCMethodName.SLOT_LEADERS: 1,
	RPCMethodName.STAKE_ACTIVATION: 1,
	RPCMethodName.STAKE_MINIMUM_DELEGATION: 1,
	RPCMethodName.SUPPLY: 1,
	RPCMethodName.TOKEN_ACCOUNT_BALANCE: 1,
	RPCMethodName.TOKEN_ACCOUNTS_BY_DELEGATE: 1,
	RPCMethodName.TOKEN_ACCOUNTS_BY_OWNER: 1,
	RPCMethodName.TOKEN_LARGEST_ACCOUNTS: 1,
	RPCMethodName.TOKEN_SUPPLY: 1,
	RPCMethodName.TRANSACTION: 10,
	RPCMethodName.TRANSACTION_COUNT: 1,
	RPCMethodName.VERSION: 1,
	RPCMethodName.VOTE_ACCOUNTS: 1,
	RPCMethodName.IS_BLOCKHASH_VALID: 1,
	RPCMethodName.MINIMUM_LEDGER_SLOT: 1,
	RPCMethodName.REQUEST_AIRDROP: 1,
	RPCMethodName.SEND_TRANSACTION: 1,
	RPCMethodName.SIMULATE_TRANSACTION: 1,
	DasMethodName.ASSET: 10,
	DasMethodName.GET_TOKEN_ACCOUNTS: 10,
	WsMethodName.ACCOUNT: 1,
	WsMethodName.BLOCK: 1,
	WsMethodName.LOGS: 1,
	WsMethodName.PROGRAM: 1,
	WsMethodName.ROOT: 1,
	WsMethodName.SIGNATURE: 1,
	WsMethodName.SLOT: 1,
	WsMethodName.SLOTS_UPDATES: 1,
	WsMethodName.VOTE: 1,
	WsMethodName.HELIUS_TRANSACTION: 1,
}



MethodName = TypeVar("MethodName", RPCMethodName, DasMethodName, WsMethodName)
class MethodMetadata(BaseModel, Generic[MethodName]):
	"""### Summary
	Metadata information sent with every request method. The generic MethodName
	is used to send the correct metadata name depending on RPC, DAS, or 
	Websockets.
	
	### Parameters
	```python
	jsonrpc: RpcVersion = "2.0"
	id: UInt32 = Field(default_factory = lambda: random.randint(1, (2**31 - 1)))
	method: MethodName
	```"""
	jsonrpc: RpcVersion = "2.0"
	id: UInt32 = Field(default_factory = lambda: random.randint(1, (2**31 - 1)))
	method: MethodName

	@field_serializer("method")
	def serialize_method_name(self, method: MethodName) -> str:
		if isinstance(method, WsMethodName):
			return method.subscribe
		return method.value



MethodResponse = TypeVar("MethodResponse", bound = Response)
class Method(BaseModel, abc.ABC, Generic[MethodResponse]):
	"""### Summary
	Base class for a solana API Method. Accepts a generic response type which
	is used to construct the response object and a RPC or DAS method metadata.
	
	### Paramters
	```python
	response_type : type[MethodResponse] = Field(exclude = True)
	metadata      : MethodMetadata[RPCMethodName] | MethodMetadata[DasMethodName]
	configuration : Configuration | None = None
	```"""
	model_config = ConfigDict(alias_generator = to_camel, populate_by_name = True)

	response_type : type[MethodResponse] = Field(exclude = True)
	metadata      : MethodMetadata[RPCMethodName] | MethodMetadata[DasMethodName]
	configuration : Configuration | None = None


	def add_configuration(self, parameters: list[Any] | dict) -> list[Any] | dict:
		if self.configuration:
			options = self.configuration.model_dump(
				exclude_none = True,
				by_alias = True,
			)
			if options:
				if isinstance(parameters, dict):
					parameters.update(options)
				else:
					parameters.append(options)
		return parameters



WsMethodResponse = TypeVar("WsMethodResponse", bound = WsResponse)
class WsMethod(BaseModel, abc.ABC, Generic[WsMethodResponse]):
	"""### Summary
	Base class for a solana API Websocket Method. Accepts a generic response
	type which is used to construct the response object and a websocket method
	metadata. Unlike the regular `Method` object, the websocket method also
	has a unsubscribe() function dependant on the specified method metadata.
	
	### Parameters
	```python
	response_type : type[WsMethodResponse] = Field(exclude = True)
	metadata      : MethodMetadata[WsMethodName]
	configuration : Configuration | None = None
	```"""
	model_config = ConfigDict(alias_generator = to_camel, populate_by_name = True)

	response_type : type[WsMethodResponse] = Field(exclude = True, frozen = True)
	metadata      : MethodMetadata[WsMethodName]
	configuration : Configuration | None = None


	def unsubscribe(self, unsubscribe_id: int) -> str:
		return json.dumps({
			"jsonrpc": "2.0",
			"id": self.metadata.id,
			"method": self.metadata.method.unsubscribe,
			"params": [unsubscribe_id]
		})
	

	def add_configuration(self, parameters: list[Any]) -> list[Any]:
		if self.configuration:
			options = self.configuration.model_dump(
				exclude_none = True,
				by_alias = True,
			)
			if options:
				parameters.append(options)
		return parameters