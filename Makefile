
all:
	@echo "Creating confs for UberHanzi deck"
	@python3 chcli.py uberhanzi --create-confs

	@echo "Creating mnemonics for UberSentences deck"
	@python3 chcli.py ubersentences --create-mnemonics

	@echo "Creating hanzi dict for YomiChan"
	@python3 chcli.py yomichan --create-hanzi-dict
	@zip output/hanzi_dict.zip output/index.json output/kanji_bank_1.json
	@rm output/index.json output/kanji_bank_1.json

server:
	@python3 chcli.py yomichan --run-server
