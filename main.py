import argparse
import random
from bitcoinlib.keys import HDKey,Key
import mnemonic as mc
from bitcoinlib.wallets import Wallet,WalletKey
import time
from ll import ll
from bitcash import *
#from bitcash.cashaddress import Address
#from bitcash.crypto import ripemd160_sha256
def format_parser():
    # 2. 定义命令行解析器对象
    parser = argparse.ArgumentParser(description='参数说明')    # description为help中添加说明

    # 3.添加命令行参数
    # 3.1 定义位置参数（命令行不可缺省）
    # 注意：位置参数不能用 - 连接词
    #   help定义内容在帮助中显示
    #   choices表示参数只能在范围内的值
    #parser.add_argument("build_path", help="操作的app应用名称")
    parser.add_argument("-t","--type",help="随机密钥生成方式 words 助记词 rint 随机数",type=str,default="rint")
    parser.add_argument("-w","--words", help="助记词个数 12  24",type=int,default=12)
    #parser.add_argument("-n","--num", help="数量",type=int,default=1)
    #parser.add_argument("action", choices=["add", "del", "update"], help="可执行操作")

    # 4.从命令行中结构化解析参数
    return parser.parse_args()

def generate_random_string_old():
    letters = "0123456789abcdef"
    px = ''.join(random.choice(letters) for _ in range(23))
    px="00000000000000000000000000000000000000001%s" % px
    return px

def generate_random_string():
    letters = "0123456789abcdef"
    px = ''.join(random.choice(letters) for _ in range(64))
    return px

if __name__ == '__main__':
   
    args = format_parser()
    count=0
    while True:
        start=time.time()
        key:HDKey=None
        if args.type=="words":
            strength=256
            if args.words==12:
                strength=128
            
            mnemonic_phrase = mc.Mnemonic().generate(strength=strength)  # strength可以是128, 160, 192, 224, 256
            #print(mnemonic_phrase)
            #mnemonic_phrase="abandon key popular depart comfort knee rain hair fame dragon clog mesh clean long mention must company render prefer radar discover view frost surprise"
            #seed = mc.Mnemonic().to_seed(mnemonic_phrase)

            #key:HDKey=HDKey.from_passphrase(passphrase=mnemonic_phrase,compressed=False,multisig=True)
            key:HDKey=HDKey.from_passphrase(mnemonic_phrase)
        
        else:
            #y = 115792089237316195423570985008687907852837564279074904382605163141518161494336
            #ran = random.randint(1, y)
            #seed = str(ran)
            #ckey = Key.from_int(ran)
            key:HDKey=HDKey(generate_random_string())
           
        
    

        #payload = list(ripemd160_sha256(key.public_byte))
        #address = Address(payload=payload, version="P2PKH")
        #print(address.cash_address())

        #print(key.subkey_for_path("m/0/0").address(compressed=True,encoding="base58"))
        #print(key.subkey_for_path("m/44'/0'/0'/0/0").address(compressed=True,encoding="base58"))
        #print(key.subkey_for_path("m/49'/0'/0'/0/0").address(compressed=True,script_type="p2sh",encoding="base58"))
        #print(key.subkey_for_path("m/84'/0'/0'/0/0").address(compressed=True,script_type="p2kh",encoding="bech32"))
        #print(key.subkey_for_path("m/0/0").address(compressed=True,script_type="p2kh",encoding="base58"))

        p2k_compressed_base58=key.address(compressed=True,script_type="p2kh",encoding="base58")
        p2s_compressed_base58=key.address(compressed=True,script_type="p2sh",encoding="base58")
        p2k_compressed_bech32=key.address(compressed=True,script_type="p2kh",encoding="bech32")
        p2s_compressed_bech32=key.address(compressed=True,script_type="p2sh",encoding="bech32")
        p2k_uncompressed_base58=key.address(compressed=False,script_type="p2kh",encoding="base58")
        p2s_uncompressed_base58=key.address(compressed=False,script_type="p2sh",encoding="base58")
        #print(key.address(compressed=True,script_type="p2kh",encoding="base58"))
        #print(key.address(compressed=True,script_type="p2sh",encoding="base58"))
        #print(key.address(compressed=True,script_type="p2kh",encoding="bech32"))
        #print(key.address(compressed=True,script_type="p2sh",encoding="bech32"))
        #print(key.address(compressed=False,script_type="p2kh",encoding="base58"))
        #print(key.address(compressed=False,script_type="p2sh",encoding="base58"))
        #print(key.address(compressed=False,script_type="p2kh",encoding="bech32"))
        #print(key.address(compressed=False,script_type="p2sh",encoding="bech32"))
        #print(key.subkey_for_path("m/0/0").address(compressed=True,encoding="base58"))

        #print("Private Key (WIF):", private_key.wif())  # 打印私钥的WIF格式

        #print("Bitcoin Address:", key.address_obj.address)      # 打印比特币地址
        #print("Bitcoin Address:", key.wif_private()) 
        addresses=[p2k_compressed_base58,p2s_compressed_base58,p2k_compressed_bech32,p2s_compressed_bech32,p2k_uncompressed_base58,p2s_uncompressed_base58]
        
        print("%s======>%s" %(key.private_hex," ".join(addresses)))
        
        result = list(set(ll) & set(addresses))
        if len(result)>0:
            file=open("output.txt", "a") 
            file.write("=====================================\n")
            file.write(" ".join(addresses)+"\n")
            file.write("Private Key --> "+key.private_hex+"\n")
            file.close()
        count+=1
        print("count: %s  speed: %s/s" %(count,int(1/(time.time()-start))))
        