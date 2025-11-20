"""
    :copyright: (c) 2022-2024, Flexxbotics, a Delaware corporation (the "COMPANY")
        All rights reserved.

        THIS SOFTWARE IS PROVIDED BY THE COMPANY ''AS IS'' AND ANY
        EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
        WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
        DISCLAIMED. IN NO EVENT SHALL THE COMPANY BE LIABLE FOR ANY
        DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
        (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
        LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
        ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
        (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
        SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
from data_models.device import Device
import json
import base64
from transformers.abstract_device import AbstractDevice
from types import SimpleNamespace
from protocols import modbus
import time
import requests


class HeidenhainTNC7_Profinet(AbstractDevice):

    def __init__(self, device: Device):
        """
        Template device class. Inherits AbstractDevice class.

        :param Device:
                    the device object

        :return:    a new instance
        """
        super().__init__(device)
        # Get meta data of the device from its attributes, this contains information such as: ip address, ports, etc
        self.meta_data = device.metaData
        self.PROFINET_PLC_IP = self.meta_data["plc_ip_address"]
        self.PLC_PORT = int(self.meta_data["plc_port"])
        self._client = modbus.ModbusTCP(self.PROFINET_PLC_IP, self.PLC_PORT)
        self._client.connect()

        self.CMD_WORD_ADDR = 0
        self.TRIGGER_ADDR = 1
        self.RESULT_ADDR = 2
        self.READY_ADDR = 3

        #modbus command addresses Automation to CNC
        self.neg_error = 0.4
        self.finished_loading = 1.1

        #modbus command addresses CNC to Automation
        self.operator_protection_OK = 0.7
        self.CNC_fault = 0.4
        self.program_in_progress = 1.1
        self.M365 = 0.5
        self.NC_part = 1.6

        self.modbus_profinet_address = 0
        self.modbus_profinet_value_address = 1

        

        # Needed for connection to TNC Remo Server to load files to memory
        self.cnc_ip_address = self.meta_data["cnc_ip_address"]
        self.host = "http://host.docker.internal"
        self.host_port = 7083
        self.base_url = self.host + ":" + str(self.host_port)

    def __del__(self):
        pass

    # ############################################################################## #
    # DEVICE COMMUNICATION METHODS
    # ############################################################################## #

    def _execute_command(self, command: str) -> str:
        """
        Executes the command sent to the device.

        :param command:
                    the command to be executed

        :return:    the response after execution of command.

        :author:    tylerjm@flexxbotics.com
        :since:     ODOULS.3 (7.1.15.3)
        """
        # Parse the command from the incoming request
        command_string = command["commandJson"]
        command_json = json.loads(command_string)
        command_name = command_json["command"]
        response = ""

        self._info(message="Sending command: " + command_string)
        try:
            pass

        except Exception as e:
            raise Exception(
                "Error when sending command, did not get response"
                + command_name
            )

        finally:
            pass

        if "ERROR" in response:
            raise Exception("Error returned from device.. " + command_name)

        return response

    def _execute_command_v2(self, command_name: str, command_args: str) -> str:
        """
        Executes the command sent to the device.

        :param command_name:
                    the command to be executed
        :param command_args:
                    json with the arguments for the command

        :return:    the response after execution of command.

        :author:    tylerjm@flexxbotics.com
        :since:     ODOULS.3 (7.1.15.3)
        """
        # Parse the command from the incoming request
        args = json.loads(command_args)
        response = ""

        self._info(message="Sending command: " + command_name)
        try:
            if command_name == "set_profinet_bit":
                self._set_profinet_bit(args["profinet_address"],args["profinet_value"])
                response = str(self._client.read_holding_register(self.modbus_profinet_address).registers)

        except Exception as e:
            raise Exception(
                "Error when sending command, did not get response from device: "
                + command_name
            )

        finally:
            pass

        if "ERROR" in response:
            raise Exception("Error returned from device... " + command_name)

        return response

    def _read_interval_data(self) -> str:
        """
        Method to read the status of the device on an interval

        :return:    status - string

        :author:    tylerjm@flexxbotics.com
        :author:    sanua@flexxbotics.com

        :since:     ODOULS.3 (7.1.15.3)
        """
        status = self.read_status()

        return status

    def _read_status(self, function: str = None) -> str:
        """
        Method to read the status of the device

        :param function:
                    Optional parameter to provide the name of a function to run - string

        :return:    status - string

        :author:    tylerjm@flexxbotics.com
        :since:     ODOULS.3 (7.1.15.3)
        """

        if function is None:
            # Write standard read status statements
            pass
        elif function == "":  # Some string
            # Write specific function call to read status
            pass
        else:
            pass

        return str("status")

    def _read_variable(self, variable_name: str, function: str = None) -> str:
        """
        Method to read the specified variable from the device

        :param variable_name:
                    The name of the variable to read - string

        :param function:
                    Optional parameter to provide the name of a function to run - string

        :return:    value - string

        :author:    tylerjm@flexxbotics.com
        :since:     ODOULS.3 (7.1.15.3)
        """
        value = ""
        if function is None:
            # Write standard read variable statements
            pass
        elif function == "":  # Some string
            # Write specific function call to read variable
            pass
        else:
            pass

        return value

    def _write_variable(self, variable_name: str, variable_value: str, function: str = None) -> str:
        """
        Method to write the specified variable on the device

        :param variable_name:
                    The name of the variable to write - string

        :param variable_value:
                    The value of the variable to write - string

        :param function:
                    Optional parameter to provide the name of a function to run - string

        :return:    value - string

        :author:    tylerjm@flexxbotics.com
        :since:     ODOULS.3 (7.1.15.3)
        """
        value = ""
        if function is None:
            # Write standard write variable statements
            pass
        elif function == "":  # Some string
            # Write specific function call to write variable
            pass
        else:
            pass

        return value

    def _write_parameter(self, parameter_name: str, parameter_value: str, function: str = None) -> str:
        """
        Method to write the specified parameter on the device

        :param parameter:
                    The parameter to write - string

        :param parameter:
                    The value of the parameter to write - string

        :param function:
                    Optional parameter to provide the name of a function to run - string

        :return:    value - string

        :author:    tylerjm@flexxbotics.com
        :since:     ODOULS.3 (7.1.15.3)
        """
        if function is None:
            # Write standard write parameter statements
            pass
        elif function == "":  # Some string
            # Write specific function call to write parameter
            pass
        else:
            pass

    def _read_parameter(self, parameter_name: str, function: str = None) -> str:
        """
        Method to read the specified parameter from the device

        :param parameter:
                    The parameter to write - string

        :param function:
                    Optional parameter to provide the name of a function to run - string

        :return:    value - string

        :author:    tylerjm@flexxbotics.com
        :since:     ODOULS.3 (7.1.15.3)
        """
        value = ""
        if function is None:
            # Write standard read variable statements
            pass
        elif function == "":  # Some string
            # Write specific function call to read variable
            pass
        else:
            pass

        return value

    def _run_program(self, function: str = None):
        """
            Method to run the active program on the device

            :param function:
                        Optional parameter to provide the name of a function to run - string

            :return:    value - string

            :author:    tylerjm@flexxbotics.com
            :since:     P.2 (7.1.16.2)
        """
        try:
            response = ""
        except Exception as e:
            response = "Error sending program"
            self._error(message=str(e))

        return response

    def _read_file_names(self) -> list:
        """
        Method to get a list of filenames from the device

        :return:    list of filenames

        :author:    tylerjm@flexxbotics.com
        :since:     KEYSTONE.4 (7.1.11.4)
        """

        # Return list of available filenames from the device
        self.programs = []

        return self.programs  # TODO is this the actual response object we want?

    def _read_file(self, file_name: str) -> str:
        """
        Method to read a file from a device

        :param file_name:
                    the name of the file to read.

        :return:    the file's data as base64 string.

        :author:    tylerjm@flexxbotics.com
        :since:     KEYSTONE.4 (7.1.11.4)
        """
        # Reads the file content off the device
        file_data = ""

        return base64.b64encode(file_data)

    def _write_file(self, file_name: str, file_data: str):
        """
        Method to write a file to a device

        :param file_name:
                    the name of the file to write.
        :param file_data:
                    the data of the file to write as base64 string.

        :author:    tylerjm@flexxbotics.com
        :since:     ODOULS.3 (7.1.15.3)
        """
        pass

    def _load_file(self, file_name: str):
        """
        Loads a file into memory on the device

        :param file_name: the name of the file to load into memory
        :return: the file name

        :author:    tylerjm@flexxbotics.com
        :since:     Q.5 (7.1.17.5)
        """
        # Connects to TNC Remo Server to load the file specified
        resp = requests.post(self.base_url + "/load", json={"filename": file_name, "ip_address": self.cnc_ip_address})

        return str(resp.json())

    # ############################################################################## #
    # INTERFACE HELPER METHODS
    #
    # These are private methods with naming convention _some_method(self). These are used to faciliate
    # any specific functions that are needed to communicate via the transformer. For example,
    # connection methods, read/write methods, specific functions, etc.
    # ############################################################################## #

    def _encode_qx(self, addr: str) -> int:
        byte, bit = addr.upper().replace("QX", "").split(".")
        return int(byte) * 8 + int(bit)

    def _set_profinet_bit(self, profinet_address:str, profinet_value:int):
        encoded_address = self._encode_qx(profinet_address)
        self._client.write_multiple_registers(self.modbus_profinet_address,[encoded_address, profinet_value])

    def read_profinet_bit(self):
        pass