from xmlrpc.client import ServerProxy


server = ServerProxy('http://localhost:9001/RPC2')

# print(server.supervisor.getState())

def get_bot_status(name):
    data = server.supervisor.getProcessInfo(name)
    return data


def start_bot(name):
    server.supervisor.startProcess(name)


def stop_bot(name):
    server.supervisor.stopProcess(name)


def clear_log(name):
    server.supervisor.clearProcessLogs(name)

# from supervisor.rpcinterface import SupervisorNamespaceRPCInterface
   
# s = SupervisorNamespaceRPCInterface(server)

# print(server.supervisor.getState())
# print(s.getState())

# print(server.supervisor.tailProcessStdoutLog('bot_user2_ses2', 0, 100))
    
    
# clear_log('user2_ses2')
