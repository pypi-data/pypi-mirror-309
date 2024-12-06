from crealand._core.bridge import _interface
from crealand._apis import _subscribe_event, _constants
from crealand._utils import _logger_setup, _utils
from typing import Callable as _Callable

_logger = _logger_setup.setup_logger()

# 人脸识别
# 机器学习
# 数字识别


class Figure:

    _digit=""
    # 打开手写数字识别教学页面
    @staticmethod
    def open_teach_page():
        _interface.call_api(
            "web-ide", 
            "api.openDigitRecognitionTeachingPage", 
            [{"name":""}]
        )

    # 打开神经网络教学页面
    @staticmethod
    def open_NN_teach_page():
        _interface.call_api(
            "web-ide", 
            "api.openNeuralNetworkTeachingPage", 
            [{"type":""}]
        )

    # 开始手写数字识别
    @staticmethod
    def start_digital_recognition():
        # 识别返回的结果需要设置保存
        # call_api_async("web-ide","api.digitRecognition",[{"type":"start"}])
        def on_result(err, data):
            if err is None:
                if data and data.get("data") and data["data"] != "":
                    Figure._digit = int(data["data"])
            else:
                _logger.error(f"Error occurred: {err},{data}")

        _subscribe_event.onAIFigureEvent("", on_result)

    # 结束手写数字识别
    @staticmethod
    def stop_digital_recognition():
        Figure._digit =""
        _interface.call_api_async(
            "web-ide", 
            "api.digitRecognition", 
            [{"type":"end"}]
        )

    # 数字识别结果
    @staticmethod
    def get_figure_value():
        return Figure._digit

    # 清除数字识别结果
    @staticmethod
    def clear_figure_value():
        Figure._digit =""
        _interface.call_api(
            "web-ide", 
            "api.digitRecognitionClear", 
            [{"type":""}]
        )

    @_utils.check_type
    @staticmethod
    def onAIFigureEvent(number: int, cb: _Callable):
        # 识别返回的结果需要设置保存
        number = max(0, min(number, 9))
        # call_api_async("web-ide","api.digitRecognition",[{"type":"start"}])
        def on_result(err, data):
            if err is None:
                if data and data.get("data") and data["data"] != "":
                    Figure._digit = int(data["data"])
                    cb()
            else:
                _logger.error(f"Error occurred: {err},{data}")

        _subscribe_event.onAIFigureEvent(number, on_result)


# 手势识别
class Gesture:
    _direction=""
    # 开始手势识别 并等待结束
    @staticmethod
    def start_gesture_recognition():
        def on_result(err, data):
            if err is None:
                if data and data.get("data") and data["data"] != "":
                    Gesture._direction = data["data"]
            else:
                _logger.error(f"Error occurred: {err},{data}")

        _subscribe_event.onAIGestureEvent("", on_result)

    # 结束手势识别
    @staticmethod
    def stop_gesture_recognition():
        Gesture._direction=""
        _interface.call_api_async(
            "web-ide", 
            "api.gestureRecognition", 
            [{"type":"end"}]
        )

    # 当前手势识别结果为
    @staticmethod
    def get_gesture_value():
        return Gesture._direction

    # 帽子积木块
    @_utils.check_type
    @staticmethod
    def onAIGestureEvent(direction:str,cb:_Callable):
        _utils.check_out_of_range("onAIGestureEvent", "direction", 
            direction, _constants.Direction)
        def on_result(err, data):
            if err is None:
                if data and data.get("data") and data["data"] != "":
                    Gesture._direction = data["data"]
                    cb()
            else:
                _logger.error(f"Error occurred: {err},{data}")

        _subscribe_event.onAIGestureEvent(direction, on_result)

# 语音识别
class Voice:
    _text=""
    # 开始语音识别
    @staticmethod
    def start_voice_recognition():
        def on_result(err, data):
            if err is None:
                if data and data.get("data") and data["data"] != "":
                    Voice._text = data["data"]
            else:
                _logger.error(f"Error occurred: {err},{data}")

        _subscribe_event.onAIAsrEvent("", on_result)


    # 结束识别
    @staticmethod
    def stop_voice_recognition():
        Voice._text =""
        _interface.call_api(
            "web-ide", 
            "api.openVoiceRecognition", 
            [{"type":"end"}]
        )

    # 语音识别结果
    @staticmethod
    def get_voice_value():
        return Voice._text


    # 打开语音识别教学页面
    @staticmethod
    def open_voice_teach_page():
        _interface.call_api(
            "web-ide", 
            "api.openVoiceRecognitionTeachingPage", 
            [{"name":""}]
        )

    # 帽子积木块
    @_utils.check_type
    @staticmethod
    def onAIAsrEvent(text: str, cb: _Callable):
        def on_result(err, data):
            if err is None:
                if data and data.get("data") and data["data"] != "":
                    Voice._text = data["data"]
                    cb()
            else:
                _logger.error(f"Error occurred: {err},{data}")

        _subscribe_event.onAIAsrEvent(text, on_result)

class Face:
    _face_data = {
        'lib_id': '',
        'name': '无匹配结果',
        'mood': '',
        'gender': '',
        'match_percent': 0
    }

    __MOOD_MAP={
        'happy': '开心',
        'calm': '平静',
        'angry': '生气',
        'surprise': '惊讶'
    }

    __GENDER_MAP={
        'male': '男',
        'female': '女'
    }

    @_utils.check_type
    @staticmethod
    def choose_face_library(id:str):
        Face._face_data['lib_id'] = id

    @_utils.check_type
    @staticmethod
    def add_face(id:str):
        Face._face_data['lib_id'] = id
        _interface.call_api('web-ide','api.addFaceToFaceLibrary',[{'id':id}])

    @_utils.check_type
    @staticmethod
    def start_face_recognition():
        
        result=_interface.call_api('web-ide','api.selectedFaceLibrary',[{'id':Face._face_data['lib_id']}])
        if result:
           data_list=result.strip().split(',')
           Face._face_data['mood']=data_list[0]
           Face._face_data['gender']=data_list[1]
           Face._face_data['match_percent']=float(data_list[2]) if data_list[2] else 0
           Face._face_data['name']=data_list[3] if data_list[3] else '无匹配结果'

        print('mood:',Face.__MOOD_MAP.get(Face._face_data['mood'],Face._face_data['mood']),'gender:',Face.__GENDER_MAP.get(Face._face_data['gender'],Face._face_data['gender']),'match_percent:',Face._face_data['match_percent'],'name:',Face._face_data['name'])
    @_utils.check_type
    @staticmethod
    def open_teach_page():
        _interface.call_api('web-ide','api.openFaceRecognitionTeachingPage',[{'name':''}])

    @_utils.check_type
    @staticmethod
    def get_name():
        return Face._face_data['name']

    @_utils.check_type
    @staticmethod
    def get_mood():
        return Face.__MOOD_MAP.get(Face._face_data['mood'],Face._face_data['mood'])
    
    @_utils.check_type
    @staticmethod
    def get_gender():
        return Face.__GENDER_MAP.get(Face._face_data['gender'],Face._face_data['gender'])

    @_utils.check_type
    @staticmethod
    def get_match_percent():
        return Face._face_data['match_percent']


class Model:

    @_utils.check_type
    @staticmethod
    def get_predict_result(id:str):
        result = _interface.call_api('web-ide','api.modelPredictionResult',[{'modelId':id}])
        return result

    @_utils.check_type
    @staticmethod
    def get_confidence_result(id:str,value:str):
        result =_interface.call_api('web-ide','api.modelPredictionResult',[{'modelId':id,'modelValue':value}])
        return result

    @_utils.check_type
    @staticmethod
    def open_teach_page():
        _interface.call_api('web-ide','api.openDecisionTreeTeachingPage',[{'name':''}])


class AIGC:
    _agent={}
    @_utils.check_type
    @staticmethod
    def bind_to_object(agent_id:int, runtime_id:int):
        AIGC._agent[runtime_id]=agent_id

    @_utils.check_type
    @staticmethod
    def start_dialogue(runtime_id:int,name:str):
        agent_id = AIGC._agent.get(runtime_id)
        _interface.call_api('web-ide','api.openDialogWithAgent',[{'objId':runtime_id,'name':name,'agentId':agent_id,'conversationId':''}])