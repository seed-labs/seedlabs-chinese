#!/bin/env python3

from SEEDBlockchain import Wallet, EmuWallet
import time, sys
import getopt

def print_usage(argv):
    cmd = sys.argv[0].replace("./", "")
    print("Usage: %s [-w <time>] [-n <total>]" % cmd)
    print("    <time>:  waiting time after sending a transaction (seconds)")
    print("    <total>: total number of transactions")
    print("    example: %s -w 0.1 -n 1000" % cmd)

def get_arguments(argv, mapping):
    # Remove 1st argument from the list of command line arguments
    argumentList = argv[1:]

    # Options and long options
    options = "hw:n:"
    long_options = ["help", "wait=", "total="]

    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)

        # checking each argument
        for arg, value in arguments:
            if arg in ("-h", "--help"):
                print_usage(sys.argv)
                exit()

            elif arg in ("-w", "--wait"):
                mapping['wait'] = value

            elif arg in ("-n", "--total"):
                mapping['total'] = value

    except getopt.error as err:
        print (str(err))

if len(sys.argv) < 2:
    print_usage(sys.argv)

# Set the default option values
options = {'wait': 1, 'total': 10000}
get_arguments(sys.argv, options)


# Create accounts using the default mnemonic phrase 
wallet = EmuWallet(chain_id=1337, url='http://10.152.0.71:8545')
wallet.addLocalAccounts()
wallet.addEmulatorAccounts()

# Send a transaction

myscope = 'all'
success = 0
failure = 0
nonces = {}
for i in range(options['total']):
   print("Transaction %d" % i)
   s_name = wallet.getRandomAccountName(scope=myscope)
   r_name = wallet.getRandomAccountName(scope=myscope)
   while r_name == s_name:
      r_name = wallet.getRandomAccountName(scope=myscope)
   
   print("==> %s ---> %s" % (s_name, r_name))

   # Get and store the nonce for each sender
   if s_name not in nonces:
       nonces[s_name] = wallet.getNonceByName(s_name)
   else:
       nonces[s_name] += 1

   recipient = wallet.getAccountAddressByName(r_name)
   try:
       wallet.sendTransaction(recipient, 0.1, sender_name=s_name, 
                   nonce=nonces[s_name], wait=False, verbose=False)
       success += 1
   except:
       print("Failed in sending this transaction")
       nonces[s_name] -= 1  # Restore the nonce value
       failure += 1
   print("** Success: %d  -- Failure: %d **" % (success, failure))

   time.sleep(float(options['wait']))
   
