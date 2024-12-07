import logging
import requests
import uuid
import json
import os
import base64

# Loggly settings
LOGGLY_TOKEN = os.getenv('LOGGLY_TOKEN')
CUSTOMER_TOKEN = os.getenv('CUSTOMER_TOKEN')
LOGGLY_TAG = 'ArmillaWatsonX'
LOGGLY_URL = f'https://logs-01.loggly.com/inputs/{CUSTOMER_TOKEN}/tag/{LOGGLY_TAG}/'
run_uuid = str(uuid.uuid4())

class LogglyHandler(logging.Handler):
    def emit(self, record):
        if not hasattr(record, 'CUSTOMER_TOKEN'):
            record.CUSTOMER_TOKEN = CUSTOMER_TOKEN
        if not hasattr(record, 'uuid'):
            record.uuid = run_uuid
        log_entry = self.format(record)
        try:
            requests.post(LOGGLY_URL, data=log_entry)
        except Exception as e:
            print(f"Failed to send log to Loggly: {e}")

def setup_logger():
    logger_type = os.getenv('LOGGER_TYPE', 'LOGGLY').upper()
    logger = logging.getLogger('armilla_logger')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    loggly_handler = LogglyHandler()
    loggly_formatter = logging.Formatter(
        '{"CUSTOMER_TOKEN": "%(CUSTOMER_TOKEN)s", "uuid": "%(uuid)s", "content": %(message)s}'
    )
    loggly_handler.setFormatter(loggly_formatter)
    logger.addHandler(loggly_handler)

    if logger_type == 'LOCAL':
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(asctime)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        print("Logging locally to console")
    else:
        print("Logging to Loggly only")

    for other_logger_name in logging.root.manager.loggerDict:
        if other_logger_name != 'armilla_logger':
            logging.getLogger(other_logger_name).setLevel(logging.ERROR)

    return logger

logger = setup_logger()

from ibm_watsonx_ai import APIClient

class ArmillaAPIClient:
    def __init__(self, credentials):
        self.client = APIClient(credentials)
        logger.info(json.dumps({
            "message": "Client successfully initialized"
        }))
    
    def __getattr__(self, name):
        original_attr = getattr(self.client, name)
        attr_str = str(original_attr)
        
        logger.info(json.dumps({
            "message": f"Retrieved attribute '{name}'",
            "attribute": attr_str
        }))

        if not callable(original_attr):
            class NestedAttributeWrapper:
                def __init__(self, nested_obj):
                    self.nested_obj = nested_obj

                def __getattr__(self, nested_name):
                    nested_attr = getattr(self.nested_obj, nested_name)
                    nested_str = str(nested_attr)
                    
                    logger.info(json.dumps({
                        "message": f"Retrieved nested attribute '{nested_name}'",
                        "attribute": nested_str
                    }))

                    if nested_name == "store_model" and callable(nested_attr):
                        def store_model_hook(*args, **kwargs):
                            model_path = kwargs.get("model")
                            max_chunk_size = 100000
                            if isinstance(model_path, str):
                                try:
                                    with open(model_path, "rb") as f:
                                        model_binary = f.read()
                                        model_base64 = base64.b64encode(model_binary).decode("utf-8")

                                    total_length = len(model_base64)
                                    total_chunks = (total_length + max_chunk_size - 1) // max_chunk_size

                                    for i in range(total_chunks):
                                        start = i * max_chunk_size
                                        end = start + max_chunk_size
                                        chunk = model_base64[start:end]

                                        logger.info(json.dumps({
                                            "message": "Model encoding chunks",
                                            "chunk_index": i + 1,
                                            "total_chunks": total_chunks,
                                            "chunk": chunk
                                        }))

                                    kwargs["model"] = model_path

                                except Exception as e:
                                    logger.error(json.dumps({
                                        "message": "Failed to encode or partition model",
                                        "error": str(e)
                                    }))
                                    raise

                            result = nested_attr(*args, **kwargs)
                            logger.info(json.dumps({
                                "message": f"{nested_name} returned",
                                "result": str(result)
                            }))
                            return result

                        return store_model_hook

                    if callable(nested_attr):
                        def hooked(*args, **kwargs):
                            serialized_args = [str(arg) for arg in args]
                            serialized_kwargs = {k: str(v) for k, v in kwargs.items()}
                            logger.info(json.dumps({
                                "message": f"Calling {nested_name}",
                                "args": serialized_args,
                                "kwargs": serialized_kwargs
                            }))
                            result = nested_attr(*args, **kwargs)
                            logger.info(json.dumps({
                                "message": f"{nested_name} returned",
                                "result": str(result)
                            }))
                            return result
                        return hooked
                    else:
                        logger.info(json.dumps({
                            "message": f"{nested_name} is not callable",
                            "value": nested_str
                        }))
                        return nested_attr
            
            return NestedAttributeWrapper(original_attr)

        else:
            def hooked(*args, **kwargs):
                serialized_args = [str(arg) for arg in args]
                serialized_kwargs = {k: str(v) for k, v in kwargs.items()}
                logger.info(json.dumps({
                    "message": f"Calling {name}",
                    "args": serialized_args,
                    "kwargs": serialized_kwargs
                }))
                result = original_attr(*args, **kwargs)
                logger.info(json.dumps({
                    "message": f"{name} returned",
                    "result": str(result)
                }))
                return result
            return hooked


from langchain_ibm import WatsonxLLM

class ArmillaWatsonxLLM(WatsonxLLM):
    def __init__(self, model_id, url, apikey, project_id, params=None):
        super().__init__(model_id=model_id, url=url, apikey=apikey, project_id=project_id, params=params)
        logger.info(json.dumps({
            "message": "Initialized WatsonxLLMWrapper",
            "model_id": model_id,
            "params": params
        }))
    
    def __getattr__(self, name):
        original_attr = getattr(self.watsonx_llm, name)
        logger.info(json.dumps({
            "message": f"Retrieved attribute '{name}'",
            "attribute": str(original_attr)
        }))

        if callable(original_attr):
            def hooked(*args, **kwargs):
                serialized_args = [str(arg) for arg in args]
                serialized_kwargs = {k: str(v) for k, v in kwargs.items()}
                
                logger.info(json.dumps({
                    "message": f"Calling {name}",
                    "args": serialized_args,
                    "kwargs": serialized_kwargs
                }))
                result = original_attr(*args, **kwargs)
                logger.info(json.dumps({
                    "message": f"{name} returned",
                    "result": str(result)
                }))
                return result
            return hooked
        else:
            logger.info(json.dumps({
                "message": f"{name} is not callable",
                "value": str(original_attr)
            }))
            return original_attr


from langchain.chains import SequentialChain

class ArmillaSequentialChain(SequentialChain):
    def __init__(self, chains, input_variables, output_variables, memory=None, verbose=False, **kwargs):
        super().__init__(
            chains=chains,
            input_variables=input_variables,
            output_variables=output_variables,
            memory=memory,
            verbose=verbose,
            **kwargs
        )
        chain_details = [
            {
                "chain_index": idx,
                "chain_name": chain.__class__.__name__,
                "input_keys": chain.input_keys,
                "output_keys": chain.output_keys
            }
            for idx, chain in enumerate(chains)
        ]

        logger.info(json.dumps({
            "message": "Initialized ArmillaSequentialChain",
            "input_variables": input_variables,
            "output_variables": output_variables,
            "memory": str(memory),
            "verbose": verbose,
            "chains": chain_details,
            "additional_kwargs": kwargs
        }))

    def invoke(self, input_data):
        logger.info(json.dumps({
            "message": "Starting ArmillaSequentialChain",
            "input_data": input_data
        }))
        
        result = super().invoke(input_data)
        
        logger.info(json.dumps({
            "message": "ArmillaSequentialChain completed",
            "output": result
        }))
        
        return result

    def __getattr__(self, name):
        original_attr = getattr(self, name)
        logger.info(json.dumps({
            "message": f"Retrieved attribute '{name}'",
            "attribute": str(original_attr)
        }))

        if callable(original_attr):
            def hooked(*args, **kwargs):
                serialized_args = [str(arg) for arg in args]
                serialized_kwargs = {k: str(v) for k, v in kwargs.items()}
                
                logger.info(json.dumps({
                    "message": f"Calling {name}",
                    "args": serialized_args,
                    "kwargs": serialized_kwargs
                }))
                result = original_attr(*args, **kwargs)
                logger.info(json.dumps({
                    "message": f"{name} returned",
                    "result": str(result)
                }))
                return result
            return hooked
        else:
            logger.info(json.dumps({
                "message": f"{name} is not callable",
                "value": str(original_attr)
            }))
            return original_attr


from langchain_core.prompts import PromptTemplate

class ArmillaPromptTemplate(PromptTemplate):
    def __init__(self, input_variables, template):
        super().__init__(input_variables=input_variables, template=template)
        logger.info(json.dumps({
            "message": "ArmillaPromptTemplate successfully initialized",
            "input_variables": input_variables,
            "template": template
        }))

    def format(self, **kwargs):
        result = super().format(**kwargs)
        logger.info(json.dumps({
            "message": "Prompt generated",
            "result": result
        }))
        return result
