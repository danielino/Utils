import logging, sys
logging.basicConfig(level=logging.DEBUG)

class Command:

    @staticmethod
    def getLogger(functionName):
        return logging.getLogger("%s.%s" % ("Command", functionName ))


    @staticmethod
    def runCommand(cmd, returnCode=False):
        import commands, re
        logger = Command.getLogger("runCommand")
        """
        loggerName = "%s::runCommand" % Command.getLogger().name
        logger = logging.getLogger(loggerName)
        """
        logger.debug("executing %s" % cmd)
        exitCode, output = commands.getstatusoutput(cmd)
        logger.debug("command executed successfully. exitCode = %d" % exitCode)

        # check if string match command not found
        if isinstance(output, str):
            if re.compile(".+command not found").findall(output):
                logger.debug("command not found")
                raise Exception(output)
            if '\n' in output:
                logger.debug("splitting lines")
                out = output.split('\n')
            else:
                out = output

        # create namedtuple
        if returnCode:
            from collections import namedtuple
            logger.debug("returnCode == True. creating namedtuple object")
            ret = dict(exitCode=exitCode, output=out)
            obj = namedtuple('command', ret.keys())(**ret)
            logger.debug("object created successfully")
            return obj
        logger.debug("returning object")
        return out


cmd = "ls -larth |grep -i anaconda | awk '{print $9}'"


res = Command.runCommand(cmd)
print res
