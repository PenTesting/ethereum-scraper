from typing import Optional

from ethscraper.domain.erc20_transfer import EthErc20Transfer
from ethscraper.domain.transaction_receipt import EthTransactionReceipt
from ethscraper.domain.transaction_receipt_log import EthTransactionReceiptLog
from ethscraper.utils import chunk_string, hex_to_dec

# https://ethereum.stackexchange.com/questions/12553/understanding-logs-and-log-blooms
TRANSFER_EVENT_TOPIC = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'


class EthErc20Processor(object):

    def filter_transfers_from_receipt(self, tx_receipt):
        # type: (EthTransactionReceipt) -> [EthErc20Transfer]

        erc20_transfers = map(lambda log: self.filter_transfer_from_receipt_log(log), tx_receipt.logs)
        erc20_transfers = filter(None, erc20_transfers)

        return erc20_transfers

    def filter_transfer_from_receipt_log(self, tx_receipt_log):
        # type: (EthTransactionReceiptLog) -> Optional[EthErc20Transfer]

        topics = tx_receipt_log.topics
        if len(topics) < 1:
            print ("Topics are empty in log {} of transaction {}".format(tx_receipt_log.log_index, tx_receipt_log.transaction_hash))
            return None

        if topics[0] == TRANSFER_EVENT_TOPIC:
            # Handle unindexed event fields
            topics_with_data = topics + self.split_to_words(tx_receipt_log.data)
            # if the number of topics and fields in data part != 4, then it's a weird event
            if len(topics_with_data) != 4:
                return None

            erc20_transfer = EthErc20Transfer()
            erc20_transfer.erc20_token = tx_receipt_log.address
            erc20_transfer.erc20_from = topics_with_data[1]
            erc20_transfer.erc20_to = topics_with_data[2]
            erc20_transfer.erc20_value = hex_to_dec(topics_with_data[3])
            erc20_transfer.erc20_tx_hash = tx_receipt_log.transaction_hash
            erc20_transfer.erc20_block_number = tx_receipt_log.block_number
            return erc20_transfer

        return None

    @staticmethod
    def split_to_words(data):
        if data and len(data) > 2:
            data_without_0x = data[2:]
            words = list(chunk_string(data_without_0x, 64))
            words_with_0x = map(lambda word: '0x' + word, words)
            return words_with_0x
        return []
