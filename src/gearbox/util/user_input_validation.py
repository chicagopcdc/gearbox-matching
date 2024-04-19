from gearbox.models import Criterion, Value, InputType
from fastapi import HTTPException
from gearbox import config
from .status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from sqlalchemy import select
from gearbox.services.criterion import get_criteria
import cdislogging
logger = cdislogging.get_logger(__name__, log_level="debug" if config.DEBUG else "info")

class UserInputValidation():
    def __init__(self):
        self.valid_criterion_format = {} #{id: {"display_name": "input_type": "values": "constraints":}}
        self.start_up_reset = True
    def error_message(self, input, display_name=None, input_type=None, values=None, id=None,):
        message = f'incorrect format in input: {input}.'

        #id does not exist
        if id:
            message += f" the id {id} in does not match any criterion"
        
        #value input_type error
        if display_name:
            message += f" the value given for: '{display_name}'"
            if input_type: 
                message += f" must be a{'n integer' if input_type == 'list' else ' string'}{' containing an integer' if input_type.lower() == 'integer' else ' containing a floating point number' if input_type == 'Float' or input_type == 'percentage'  else ''}"
            if values:
                message += f" is not one of the valid options: {values}"
            

        raise HTTPException(HTTP_400_BAD_REQUEST, message)

    def validate_input(self, user_input):
        
        if not self.valid_criterion_format:
            raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, "the validation data has not been setup or failed, user-input cannot be submitted")

        for input in user_input:
            
            if (len(input) != 2
                or "id" not in input 
                or "value" not in input 
                or not isinstance(input["id"], int)
                or (not isinstance(input["value"], str) and not isinstance(input["value"], int)) 
               ):
                self.error_message(input)

            id = str(input["id"])
            value = input["value"]

            if id in self.valid_criterion_format:
                
                criterion = self.valid_criterion_format[id]
                display_name = criterion["display_name"]
                input_type = criterion["input_type"]
                options = criterion['values']

                if input_type == 'list':
                    if not isinstance(value, int):
                        self.error_message(input, display_name, input_type)
                    
                    if value not in options:
                        self.error_message(input, display_name, values=options)
            
                else:

                    if not isinstance(value, str):
                        self.error_message(input, display_name, input_type)

                    if input_type.lower() == "integer":
                        try:
                            int(value)
                        except ValueError:
                            self.error_message(input, display_name, input_type)
                    
                    else:
                        try:
                            float(value)
                        except ValueError:
                            self.error_message(input, display_name, input_type)
                    
            else:
                self.error_message(input, id=id)

    async def update_validation(self, session):
        self.start_up_reset = False
        logger.info("User input validation data update STARTING")
        self.valid_criterion_format = {}
        try:
            #valid_criterion_format = {} #{id: {"display_name": "input_type": "values": "constraints":}}
            criteria = await get_criteria(session)
            
            for criterion in criteria:
                self.valid_criterion_format[str(criterion.id)] = {
                    "display_name": criterion.display_name, 
                    "input_type": criterion.input_type.data_type, 
                    "values": set(value.value_id for value in criterion.values) if criterion.values else None,
                    "constraints": None 
                }
        except Exception as e:
            logger.error(f"User input validation ran into an ERROR: {e}")
            logger.error(f"Maintaining previous validation Data")

        message = "User input validation update COMPLETED"

        logger.info(message)

        return message


user_input_validation = UserInputValidation()


"""

print(criterion.id, criterion.display_name, criterion.input_type.data_type, [value.value_id for value in criterion.values])

[{id: 3, value: 1}]

[{id: 1, value: "5"}, {id: 3, value: 1}]

from criterion table:

id = 1 input_type_id = 6


"""