#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2025 Mitsuo KONDOU.
# This software is released under the not MIT License.
# Permission from the right holder is required for use.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------

import sys
import os
import time
import datetime
import codecs
import shutil

import json
import queue
import base64



# freeai チャットボット
import google.generativeai as genai
#import google.ai.generativelanguage as glm

import speech_bot_freeai_key as freeai_key



# base64 encode
def base64_encode(file_path):
    with open(file_path, "rb") as input_file:
        return base64.b64encode(input_file.read()).decode('utf-8')



class _freeaiAPI:

    def __init__(self, ):
        self.log_queue              = None
        self.bot_auth               = None

        self.temperature            = 0.8
        self.timeOut                = 180

        self.freeai_api_type        = 'freeai'
        self.freeai_default_gpt     = 'auto'
        self.freeai_default_class   = 'auto'
        self.freeai_auto_continue   = 3
        self.freeai_max_step        = 10
        self.freeai_max_session     = 5
       
        self.freeai_key_id          = None

        self.freeai_a_enable        = False
        self.freeai_a_nick_name     = ''
        self.freeai_a_model         = None
        self.freeai_a_token         = 0

        self.freeai_b_enable        = False
        self.freeai_b_nick_name     = ''
        self.freeai_b_model         = None
        self.freeai_b_token         = 0

        self.freeai_v_enable        = False
        self.freeai_v_nick_name     = ''
        self.freeai_v_model         = None
        self.freeai_v_token         = 0

        self.freeai_x_enable        = False
        self.freeai_x_nick_name     = ''
        self.freeai_x_model         = None
        self.freeai_x_token         = 0

        self.safety_settings        = [ {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_NONE" },
                                        {"category": "HARM_CATEGORY_HARASSMENT","threshold": "BLOCK_NONE" },
                                        {"category": "HARM_CATEGORY_HATE_SPEECH","threshold": "BLOCK_NONE" },
                                        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE" },
                                        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE" }, ]

        self.history                = []

        self.seq                    = 0
        self.reset()

    def init(self, log_queue=None, ):
        self.log_queue = log_queue
        return True

    def reset(self, ):
        self.history                = []
        return True

    def print(self, session_id='admin', text='', ):
        print(text, flush=True)
        if (session_id == 'admin') and (self.log_queue is not None):
            try:
                self.log_queue.put(['chatBot', text + '\n'])
            except:
                pass

    def stream(self, session_id='admin', text='', ):
        print(text, end='', flush=True)
        if (session_id == 'admin') and (self.log_queue is not None):
            try:
                self.log_queue.put(['chatBot', text])
            except:
                pass

    def authenticate(self, api,
                     freeai_api_type,
                     freeai_default_gpt, freeai_default_class,
                     freeai_auto_continue,
                     freeai_max_step, freeai_max_session,

                     freeai_key_id,

                     freeai_a_nick_name, freeai_a_model, freeai_a_token, 
                     freeai_b_nick_name, freeai_b_model, freeai_b_token, 
                     freeai_v_nick_name, freeai_v_model, freeai_v_token, 
                     freeai_x_nick_name, freeai_x_model, freeai_x_token, 
                    ):

        # 設定

        # 認証
        self.bot_auth                 = None
        self.freeai_key_id            = freeai_key_id

        self.freeai_default_gpt       = freeai_default_gpt
        self.freeai_default_class     = freeai_default_class
        if (str(freeai_auto_continue) != 'auto'):
            self.freeai_auto_continue = int(freeai_auto_continue)
        if (str(freeai_max_step)      != 'auto'):
            self.freeai_max_step      = int(freeai_max_step)
        if (str(freeai_max_session) != 'auto'):
            self.freeai_max_session   = int(freeai_max_session)

        # freeai チャットボット
        if (freeai_a_nick_name != ''):
            self.freeai_a_enable     = False
            self.freeai_a_nick_name  = freeai_a_nick_name
            self.freeai_a_model      = freeai_a_model
            self.freeai_a_token      = int(freeai_a_token)

        if (freeai_b_nick_name != ''):
            self.freeai_b_enable     = False
            self.freeai_b_nick_name  = freeai_b_nick_name
            self.freeai_b_model      = freeai_b_model
            self.freeai_b_token      = int(freeai_b_token)

        if (freeai_v_nick_name != ''):
            self.freeai_v_enable     = False
            self.freeai_v_nick_name  = freeai_v_nick_name
            self.freeai_v_model      = freeai_v_model
            self.freeai_v_token      = int(freeai_v_token)

        if (freeai_x_nick_name != ''):
            self.freeai_x_enable     = False
            self.freeai_x_nick_name  = freeai_x_nick_name
            self.freeai_x_model      = freeai_x_model
            self.freeai_x_token      = int(freeai_x_token)

        # API-KEYの設定
        if (freeai_key_id[:1] == '<'):
            return False
        try:
            genai.configure(api_key=freeai_key_id, ) 
        except Exception as e:
            print('configure error', e)
            return False

        # モデル一覧
        hit = False
        #try:
        if False:
            for m in genai.list_models():
                #print(m.supported_generation_methods)
                if 'generateContent' in m.supported_generation_methods:
                    model = m.name.replace('models/', '')
                    #print(model)
                    if (model == self.freeai_a_model):
                        #print(model)
                        self.freeai_a_enable = True
                        hit = True
                    if (model == self.freeai_b_model):
                        #print(model)
                        self.freeai_b_enable = True
                        hit = True
                    if (model == self.freeai_v_model):
                        #print(model)
                        self.freeai_v_enable = True
                        hit = True
                    if (model == self.freeai_x_model):
                        #print(model)
                        self.freeai_x_enable = True
                        hit = True
        #except Exception as e:
        #    print('list_models error', e)

        self.freeai_a_enable = True
        self.freeai_b_enable = True
        self.freeai_v_enable = True
        self.freeai_x_enable = True
        hit = True

        if (hit == True):
            self.bot_auth = True
            return True
        else:
            return False

    def setTimeOut(self, timeOut=120, ):
        self.timeOut = timeOut

    def text_replace(self, text=''):
        if "```" not in text:
            return self.text_replace_sub(text)
        else:
            # ```が2か所以上含まれている場合の処理
            first_triple_quote_index = text.find("```")
            last_triple_quote_index = text.rfind("```")
            if first_triple_quote_index == last_triple_quote_index:
                return self.text_replace_sub(text)
            # textの先頭から最初の```までをtext_replace_subで成形
            text_before_first_triple_quote = text[:first_triple_quote_index]
            formatted_before = self.text_replace_sub(text_before_first_triple_quote)
            formatted_before = formatted_before.strip() + '\n'
            # 最初の```から最後の```の直前までを文字列として抽出
            code_block = text[first_triple_quote_index : last_triple_quote_index]
            code_block = code_block.strip() + '\n'
            # 最後の```以降の部分をtext_replace_subで成形
            text_after_last_triple_quote = text[last_triple_quote_index:]
            formatted_after = self.text_replace_sub(text_after_last_triple_quote)
            formatted_after = formatted_after.strip() + '\n'
            # 結果を結合して戻り値とする
            return (formatted_before + code_block + formatted_after).strip()

    def text_replace_sub(self, text='', ):
        if (text.strip() == ''):
            return ''

        text = text.replace('\r', '')

        text = text.replace('。', '。\n')
        text = text.replace('?', '?\n')
        text = text.replace('？', '?\n')
        text = text.replace('!', '!\n')
        text = text.replace('！', '!\n')
        text = text.replace('。\n」','。」')
        text = text.replace('。\n"' ,'。"')
        text = text.replace("。\n'" ,"。'")
        text = text.replace('?\n」','?」')
        text = text.replace('?\n"' ,'?"')
        text = text.replace("?\n'" ,"?'")
        text = text.replace('!\n」','!」')
        text = text.replace('!\n"' ,'!"')
        text = text.replace("!\n'" ,"!'")
        text = text.replace("!\n=" ,"!=")
        text = text.replace("!\n--" ,"!--")

        text = text.replace('\n \n ' ,'\n')
        text = text.replace('\n \n' ,'\n')

        hit = True
        while (hit == True):
            if (text.find('\n\n')>0):
                hit = True
                text = text.replace('\n\n', '\n')
            else:
                hit = False

        return text.strip()

    def history_add(self, history=[], sysText=None, reqText=None, inpText='こんにちは', ):
        res_history = history

        # sysText, reqText, inpText -> history
        if (sysText is not None) and (sysText.strip() != ''):
            if (len(res_history) > 0):
                if (sysText.strip() != res_history[0]['content'].strip()):
                    res_history = []
            if (len(res_history) == 0):
                self.seq += 1
                dic = {'seq': self.seq, 'time': time.time(), 'role': 'system', 'name': '', 'content': sysText.strip() }
                res_history.append(dic)
        if (reqText is not None) and (reqText.strip() != ''):
            self.seq += 1
            dic = {'seq': self.seq, 'time': time.time(), 'role': 'user', 'name': '', 'content': reqText.strip() }
            res_history.append(dic)
        if (inpText.strip() != ''):
            self.seq += 1
            dic = {'seq': self.seq, 'time': time.time(), 'role': 'user', 'name': '', 'content': inpText.rstrip() }
            res_history.append(dic)

        return res_history

    def history_zip1(self, history=[]):
        res_history = history

        if (len(res_history) > 0):
            for h in reversed(range(len(res_history))):
                tm = res_history[h]['time']
                if ((time.time() - tm) > 900): #15分で忘れてもらう
                    if (h != 0):
                        del res_history[h]
                    else:
                        if (res_history[0]['role'] != 'system'):
                            del res_history[0]

        return res_history

    def history_zip2(self, history=[], leave_count=4, ):
        res_history = history

        if (len(res_history) > 6):
            for h in reversed(range(2, len(res_history) - leave_count)):
                del res_history[h]

        return res_history

    def history2msg_text(self, history=[], ):
        # 過去メッセージ追加
        msg_text = ''
        if (len(history) > 2):
            msg_text += "''' これは過去の会話履歴です。\n"
            for m in range(len(history) - 2):
                role    = history[m+1].get('role','')
                content = history[m+1].get('content','')
                name    = history[m+1].get('name','')
                if (role != 'system'):
                    # 全てユーザーメッセージにて処理
                    if (name is None) or (name == ''):
                        msg_text += '(' + role + ')' + '\n' + content + '\n'
                    else:
                        if (role == 'function_call'):
                            msg_text += '(function ' + name + ' call)'  + '\n' + content + '\n'
                        else:
                            msg_text += '(function ' + name + ' result) ' + '\n' + content + '\n'
            msg_text += "''' 会話履歴はここまでです。\n"
            msg_text += "\n"
        m = len(history) - 1
        msg_text += history[m].get('content', '')
        #print(msg_text)

        return msg_text



    def files_check(self, filePath=[], ):
        upload_files = []
        image_urls   = []

        # filePath確認
        if (len(filePath) > 0):
            try:

                for file_name in filePath:
                    if (os.path.isfile(file_name)):
                        if (os.path.getsize(file_name) <= 20000000):

                            upload_files.append(file_name)
                            file_ext = os.path.splitext(file_name)[1][1:].lower()
                            if (file_ext in ('jpg', 'jpeg', 'png')):
                                base64_text = base64_encode(file_name)
                                if (file_ext in ('jpg', 'jpeg')):
                                    url = {"url": f"data:image/jpeg;base64,{base64_text}"}
                                    image_url = {'type':'image_url', 'image_url': url}
                                    image_urls.append(image_url)
                                if (file_ext == 'png'):
                                    url = {"url": f"data:image/png;base64,{base64_text}"}
                                    image_url = {'type':'image_url', 'image_url': url}
                                    image_urls.append(image_url)

            except Exception as e:
                print(e)

        return upload_files, image_urls



    def run_gpt(self, chat_class='chat', model_select='auto',
                nick_name=None, model_name=None,
                session_id='admin', history=[], function_modules=[],
                sysText=None, reqText=None, inpText='こんにちは',
                upload_files=[], image_urls=[], 
                temperature=0.8, max_step=10, jsonSchema=None, ):

        # 戻り値
        res_text        = ''
        res_path        = ''
        res_files       = []
        res_name        = None
        res_api         = None
        res_history     = history

        if (self.bot_auth is None):
            self.print(session_id, ' FreeAI  : Not Authenticate Error !')
            return res_text, res_path, res_name, res_api, res_history

        # モデル 設定
        res_name = self.freeai_a_nick_name
        res_api  = self.freeai_a_model
        if  (chat_class == 'freeai'):
            if (self.freeai_b_enable == True):
                res_name = self.freeai_b_nick_name
                res_api  = self.freeai_b_model

        # モデル 補正 (assistant)
        if ((chat_class == 'assistant') \
        or  (chat_class == 'コード生成') \
        or  (chat_class == 'コード実行') \
        or  (chat_class == '文書検索') \
        or  (chat_class == '複雑な会話') \
        or  (chat_class == 'アシスタント') \
        or  (model_select == 'x')):
            if (self.freeai_x_enable == True):
                res_name = self.freeai_x_nick_name
                res_api  = self.freeai_x_model

        # model 指定
        if (self.freeai_a_nick_name != ''):
            if (inpText.strip()[:len(self.freeai_a_nick_name)+1].lower() == (self.freeai_a_nick_name.lower() + ',')):
                inpText = inpText.strip()[len(self.freeai_a_nick_name)+1:]
        if (self.freeai_b_nick_name != ''):
            if (inpText.strip()[:len(self.freeai_b_nick_name)+1].lower() == (self.freeai_b_nick_name.lower() + ',')):
                inpText = inpText.strip()[len(self.freeai_b_nick_name)+1:]
                if   (self.freeai_b_enable == True):
                        res_name = self.freeai_b_nick_name
                        res_api  = self.freeai_b_model
        if (self.freeai_v_nick_name != ''):
            if (inpText.strip()[:len(self.freeai_v_nick_name)+1].lower() == (self.freeai_v_nick_name.lower() + ',')):
                inpText = inpText.strip()[len(self.freeai_v_nick_name)+1:]
                if   (self.freeai_v_enable == True):
                    if  (len(image_urls) > 0) \
                    and (len(image_urls) == len(upload_files)):
                        res_name = self.freeai_v_nick_name
                        res_api  = self.freeai_v_model
                elif (self.freeai_x_enable == True):
                        res_name = self.freeai_x_nick_name
                        res_api  = self.freeai_x_model
        if (self.freeai_x_nick_name != ''):
            if (inpText.strip()[:len(self.freeai_x_nick_name)+1].lower() == (self.freeai_x_nick_name.lower() + ',')):
                inpText = inpText.strip()[len(self.freeai_x_nick_name)+1:]
                if   (self.freeai_x_enable == True):
                        res_name = self.freeai_x_nick_name
                        res_api  = self.freeai_x_model
                elif (self.freeai_b_enable == True):
                        res_name = self.freeai_b_nick_name
                        res_api  = self.freeai_b_model
        if   (inpText.strip()[:5].lower() == ('riki,')):
            inpText = inpText.strip()[5:]
            if   (self.freeai_x_enable == True):
                        res_name = self.freeai_x_nick_name
                        res_api  = self.freeai_x_model
            elif (self.freeai_b_enable == True):
                        res_name = self.freeai_b_nick_name
                        res_api  = self.freeai_b_model
        elif (inpText.strip()[:7].lower() == ('vision,')):
            inpText = inpText.strip()[7:]
            if   (self.freeai_v_enable == True):
                if  (len(image_urls) > 0) \
                and (len(image_urls) == len(upload_files)):
                        res_name = self.freeai_v_nick_name
                        res_api  = self.freeai_v_model
            elif (self.freeai_x_enable == True):
                        res_name = self.freeai_x_nick_name
                        res_api  = self.freeai_x_model
        elif (inpText.strip()[:10].lower() == ('assistant,')):
            inpText = inpText.strip()[10:]
            if (self.freeai_x_enable == True):
                        res_name = self.freeai_x_nick_name
                        res_api  = self.freeai_x_model
            elif (self.freeai_b_enable == True):
                        res_name = self.freeai_b_nick_name
                        res_api  = self.freeai_b_model
        elif (inpText.strip()[:7].lower() == ('openai,')):
            inpText = inpText.strip()[7:]
        elif (inpText.strip()[:6].lower() == ('azure,')):
            inpText = inpText.strip()[6:]
        elif (inpText.strip()[:7].lower() == ('claude,')):
            inpText = inpText.strip()[7:]
        elif (inpText.strip()[:7].lower() == ('gemini,')):
            inpText = inpText.strip()[7:]
        elif (inpText.strip()[:11].lower() == ('perplexity,')):
            inpText = inpText.strip()[11:]
        elif (inpText.strip()[:5].lower() == ('pplx,')):
            inpText = inpText.strip()[5:]
        elif (inpText.strip()[:7].lower() == ('ollama,')):
            inpText = inpText.strip()[7:]
        elif (inpText.strip()[:6].lower() == ('local,')):
            inpText = inpText.strip()[6:]
        elif (inpText.strip()[:7].lower() == ('freeai,')):
            inpText = inpText.strip()[7:]
        elif (inpText.strip()[:5].lower() == ('free,')):
            inpText = inpText.strip()[5:]
        elif (inpText.strip()[:6].lower() == ('plamo,')):
            inpText = inpText.strip()[6:]

        # モデル 未設定時
        if (res_api is None):
            res_name = self.freeai_a_nick_name
            res_api  = self.freeai_a_model
            if (self.freeai_b_enable == True):
                if (len(upload_files) > 0) \
                or (len(inpText) > 1000):
                    res_name = self.freeai_b_nick_name
                    res_api  = self.freeai_b_model

        # モデル 補正 (vision)
        if  (len(image_urls) > 0) \
        and (len(image_urls) == len(upload_files)):
            if   (self.freeai_v_enable == True):
                res_name = self.freeai_v_nick_name
                res_api  = self.freeai_v_model
            elif (self.freeai_x_enable == True):
                res_name = self.freeai_x_nick_name
                res_api  = self.freeai_x_model

        # history 追加・圧縮 (古いメッセージ)
        res_history = self.history_add(history=res_history, sysText=sysText, reqText=reqText, inpText=inpText, )
        res_history = self.history_zip1(history=res_history, )

        # メッセージ作成
        msg_text = self.history2msg_text(history=res_history, )

        # ファイル添付
        req_files = []
        for file_name in upload_files:
            if (os.path.isfile(file_name)):
                #if (file_name[-4:].lower() in ['.jpg', '.png']):
                #    img = Image.open(file_name)
                #    request.append(img)
                #else:

                    # 確認
                    hit = False
                    up_files = genai.list_files()
                    for upf in up_files:
                        if (upf.display_name == os.path.basename(file_name)):
                            hit = True
                            upload_obj = genai.get_file(upf.name)
                            req_files.append(upload_obj)
                            break

                    # ***free特別処理*** 毎回送信
                    #if (hit == False):
                    if True:

                        # 送信
                        self.print(session_id, f" FreeAI  : Upload file '{ file_name }'.")
                        upload_file = genai.upload_file(file_name, display_name=os.path.basename(file_name), )
                        upload_obj  = genai.get_file(upload_file.name)

                        # 待機
                        self.print(session_id, f" FreeAI  : Upload processing ... '{ upload_file.name }'")
                        chkTime = time.time()
                        while ((time.time() - chkTime) < 120) and (upload_file.state.name == "PROCESSING"):
                            time.sleep(5.00)
                        if (upload_file.state.name == "PROCESSING"):
                            self.print(session_id, ' FreeAI  : Upload timeout. (120s)')
                            return res_text, res_path, res_name, res_api, res_history

                        # 完了
                        self.print(session_id, ' FreeAI  : Upload complete.')
                        req_files.append(upload_obj)

        # ***free特別処理*** tools未対応?
        tools = []
        if True:

            # tools
            #tools = [{"name":'code_execution'}]
            for module_dic in function_modules:
                func_dic = module_dic['function']
                func_str = json.dumps(func_dic, ensure_ascii=False, )
                func_str = func_str.replace('"type"', '"type_"')
                func_str = func_str.replace('"object"', '"OBJECT"')
                func_str = func_str.replace('"string"', '"STRING"')
                func     = json.loads(func_str)
                tools.append(func)

        # freeai 設定
        if (jsonSchema is None) or (jsonSchema == ''):
            generation_config_normal = {
                "temperature": temperature,
                "top_p": 0.95,
                "top_k": 32,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }
            freeai = genai.GenerativeModel(
                            model_name=res_api,
                            generation_config=generation_config_normal,
                            system_instruction=sysText, tools=tools, 
                            safety_settings=self.safety_settings, )
        else:
            # 2024/09/04時点 スキーマ実行時はtools使えない！
            tools = []
            generation_config_json = {
                "temperature": temperature,
                "top_p": 0.95,
                "top_k": 32,
                "max_output_tokens": 8192,
                "response_mime_type": "application/json",
            }
            freeai = genai.GenerativeModel( 
                            model_name=res_api,
                            generation_config=generation_config_json,
                            system_instruction=sysText, tools=tools, 
                            safety_settings=self.safety_settings, )

        # # ファイル削除
        # files = genai.list_files()
        # for f in files:
        #    self.print(session_id, f" FreeAI  : Delete file { f.name }.")
        #    genai.delete_file(f.name)

        request = []
        request.append(msg_text)
        request = list(req_files + request)

        # freeai
        #chat = freeai.start_chat(history=history, )
        chat = freeai.start_chat(history=[], )

        # ストリーム実行?
        if (session_id == 'admin'):
            stream = True
        else:
            stream = False
        #print('stream = False, ')
        #stream = False

        # ***free特別処理***
        #res_name = self.freeai_a_nick_name
        #res_api  = self.freeai_a_model
        #print('stream = False, ')
        stream = False

        # 実行ループ
        #try:
        if True:

            n = 0
            function_name = ''
            while (function_name != 'exit') and (n < int(max_step)):

                # 結果
                res_role      = None
                res_content   = ''
                tool_calls    = []

                # GPT
                n += 1
                self.print(session_id, f" FreeAI  : { res_api }, pass={ n }, ")

                # 結果
                content_text  = ''
                content_parts = None

                # Stream 表示
                if (stream == True):

                    chkTime  = time.time()
                    content  = {"role": "user", "parts": request }
                    streams  = chat.send_message(content=content, stream=stream, )

                    # Stream 処理
                    for chunk in streams:
                        if ((time.time() - chkTime) > self.timeOut):
                            break

                        for p in range(len(chunk.candidates[0].content.parts)):
                            delta_text = chunk.candidates[0].content.parts[p].text
                            if (delta_text is not None):
                                if (delta_text != ''):
                                    self.stream(session_id, delta_text)
                                    content_text += delta_text

                        if (content_text == ''):
                            content_parts = chunk.candidates[0].content.parts

                    # 改行
                    if (content_text != ''):
                        self.print(session_id, )

                # 通常実行
                if (stream == False):
                        content  = {"role": "user", "parts": request }
                        response = chat.send_message(content=content, stream=stream, )
                        #print(response)

                        for p in range(len(response.candidates[0].content.parts)):
                            chunk_text = response.candidates[0].content.parts[p].text
                            if (chunk_text is not None):
                                if (chunk_text.strip() != ''):
                                    self.print(session_id, chunk_text)
                                    if (content_text != ''):
                                        content_text += '\n'
                                    content_text += chunk_text

                        if (content_text == ''):
                            content_parts = response.candidates[0].content.parts

                # 共通 text 処理
                if (content_text != ''):
                    if (content_text[:9]  != "```python") \
                    or (content_text[-3:] != "```"):
                        res_role    = 'assistant'
                    else:
                        time.sleep(5.00)
                    res_content += content_text + '\n'

                # 共通 parts 処理
                if (content_parts is not None):
                    try:
                        for parts in content_parts:
                            f_name   = parts.function_call.name
                            f_args   = parts.function_call.args
                            f_kwargs = None
                            if (f_name != '') and (f_args is not None):
                                json_dic = {}
                                for key,value in f_args.items():
                                    json_dic[key] = value
                                f_kwargs = json.dumps(json_dic, ensure_ascii=False, )
                                tool_calls.append({"id": parts, "type": "function", "function": { "name": f_name, "arguments": f_kwargs } })
                    except Exception as e:
                        print(e)

                # function 指示?
                if (len(tool_calls) > 0):
                    self.print(session_id, )

                    # メッセージ格納
                    request = []
                    #request.append(inpText)
                    #if (content_parts is not None):
                    #    for parts in content_parts:
                    #        request.append(parts)

                    for tc in tool_calls:
                        f_id     = tc.get('id')
                        f_name   = tc['function'].get('name')
                        f_kwargs = tc['function'].get('arguments')

                        hit = False

                        for module_dic in function_modules:
                            if (f_name == module_dic['func_name']):
                                hit = True
                                self.print(session_id, f" FreeAI  :   function_call '{ module_dic['script'] }' ({ f_name })")
                                self.print(session_id, f" FreeAI  :   → { f_kwargs }")

                                # メッセージ追加格納
                                self.seq += 1
                                dic = {'seq': self.seq, 'time': time.time(), 'role': 'function_call', 'name': f_name, 'content': f_kwargs }
                                res_history.append(dic)

                                # function 実行
                                try:
                                    ext_func_proc  = module_dic['func_proc']
                                    res_json = ext_func_proc( f_kwargs )
                                except Exception as e:
                                    print(e)
                                    # エラーメッセージ
                                    dic = {}
                                    dic['error'] = e 
                                    res_json = json.dumps(dic, ensure_ascii=False, )

                                # tool_result
                                self.print(session_id, f" FreeAI  :   → { res_json }")
                                self.print(session_id, )

                                # メッセージ追加格納
                                res_dic  = json.loads(res_json)
                                res_list = []
                                for key,value in res_dic.items():
                                    res_list.append({ "key": key, "value": { "string_value": value } })
                                parts = {
                                            "function_response": {
                                                "name": f_name, 
                                                "response": {
                                                    "fields": res_list
                                                }
                                            }
                                        }
                                request.append(parts)
    
                                self.seq += 1
                                dic = {'seq': self.seq, 'time': time.time(), 'role': 'function', 'name': f_name, 'content': res_json }
                                res_history.append(dic)

                                # パス情報確認
                                try:
                                    dic  = json.loads(res_json)
                                    path = dic['image_path']
                                    if (path is None):
                                        path = dic.get('excel_path')
                                    if (path is not None):
                                        res_path = path
                                        res_files.append(path)
                                        res_files = list(set(res_files))
                                except:
                                    pass

                                break

                        if (hit == False):
                            print(tc, )
                            self.print(session_id, f" FreeAI  :   function_call Error ! ({ f_name })")
                            print(res_role, res_content, f_name, f_kwargs, )
                            break
                
                # GPT 会話終了
                elif (res_role == 'assistant') and (res_content != ''):
                    function_name   = 'exit'
                    self.print(session_id, f" FreeAI  : { res_name.lower() } complite.")

            # 正常回答
            if (res_content != ''):
                #self.print(session_id, res_content.rstrip())
                res_text += res_content.rstrip()

            # 異常回答
            else:
                self.print(session_id, ' FreeAI  : Error !')

            # History 追加格納
            if (res_text.strip() != ''):
                #res_history = chat.history

                self.seq += 1
                dic = {'seq': self.seq, 'time': time.time(), 'role': 'assistant', 'name': '', 'content': res_text }
                res_history.append(dic)

            # # ファイル削除
            # files = genai.list_files()
            # for f in files:
            #    self.print(session_id, f" FreeAI  : Delete file { f.name }.")
            #    genai.delete_file(f.name)

        #except Exception as e:
        #    print(e)
        #    res_text = ''

        return res_text, res_path, res_files, res_name, res_api, res_history



    def chatBot(self, chat_class='auto', model_select='auto',
                session_id='admin', history=[], function_modules=[],
                sysText=None, reqText=None, inpText='こんにちは', 
                filePath=[],
                temperature=0.8, max_step=10, jsonSchema=None,
                inpLang='ja-JP', outLang='ja-JP', ):

        # 戻り値
        res_text    = ''
        res_path    = ''
        res_files   = []
        nick_name   = None
        model_name  = None
        res_history = history

        if (sysText is None) or (sysText == ''):
            sysText = 'あなたは美しい日本語を話す賢いアシスタントです。'

        if (self.bot_auth is None):
            self.print(session_id, ' FreeAI : Not Authenticate Error !')
            return res_text, res_path, nick_name, model_name, res_history

        # ファイル分離
        upload_files    = []
        image_urls      = []
        try:
            upload_files, image_urls = self.files_check(filePath=filePath, )
        except Exception as e:
            print(e)

        # 実行モデル判定
        #nick_name  = 'auto'
        #model_name = 'auto'

        # freeai
        res_text, res_path, res_files, nick_name, model_name, res_history = \
        self.run_gpt(   chat_class=chat_class, model_select=model_select,
                        nick_name=nick_name, model_name=model_name,
                        session_id=session_id, history=res_history, function_modules=function_modules,
                        sysText=sysText, reqText=reqText, inpText=inpText,
                        upload_files=upload_files, image_urls=image_urls,
                        temperature=temperature, max_step=max_step, jsonSchema=jsonSchema, )

        # 文書成形
        text = self.text_replace(text=res_text, )
        if (text.strip() != ''):
            res_text = text
        else:
            res_text = '!'

        return res_text, res_path, res_files, nick_name, model_name, res_history



if __name__ == '__main__':

        #freeaiAPI = speech_bot_freeai.ChatBotAPI()
        freeaiAPI = _freeaiAPI()

        api_type = freeai_key.getkey('freeai','freeai_api_type')
        print(api_type)

        log_queue = queue.Queue()
        res = freeaiAPI.init(log_queue=log_queue, )

        res = freeaiAPI.authenticate('freeai',
                            api_type,
                            freeai_key.getkey('freeai','freeai_default_gpt'), freeai_key.getkey('freeai','freeai_default_class'),
                            freeai_key.getkey('freeai','freeai_auto_continue'),
                            freeai_key.getkey('freeai','freeai_max_step'), freeai_key.getkey('freeai','freeai_max_session'),
                            freeai_key.getkey('freeai','freeai_key_id'),
                            freeai_key.getkey('freeai','freeai_a_nick_name'), freeai_key.getkey('freeai','freeai_a_model'), freeai_key.getkey('freeai','freeai_a_token'),
                            freeai_key.getkey('freeai','freeai_b_nick_name'), freeai_key.getkey('freeai','freeai_b_model'), freeai_key.getkey('freeai','freeai_b_token'),
                            freeai_key.getkey('freeai','freeai_v_nick_name'), freeai_key.getkey('freeai','freeai_v_model'), freeai_key.getkey('freeai','freeai_v_token'),
                            freeai_key.getkey('freeai','freeai_x_nick_name'), freeai_key.getkey('freeai','freeai_x_model'), freeai_key.getkey('freeai','freeai_x_token'),
                            )
        print('authenticate:', res, )
        if (res == True):
            
            function_modules = []
            filePath         = []

            if True:
                import    speech_bot_function
                botFunc = speech_bot_function.botFunction()

                res, msg = botFunc.functions_load(
                    functions_path='_extensions/function/', secure_level='low', )
                if (res != True) or (msg != ''):
                    print(msg)
                    print()

                for module_dic in botFunc.function_modules:
                    if (module_dic['onoff'] == 'on'):
                        function_modules.append(module_dic)

            if True:
                sysText = None
                reqText = ''
                inpText = 'おはようございます。'
                #inpText = 'f-flash,兵庫県三木市の天気？'
                print()
                print('[Request]')
                print(reqText, inpText )
                print()
                res_text, res_path, res_files, res_name, res_api, freeaiAPI.history = \
                    freeaiAPI.chatBot(  chat_class='auto', model_select='auto', 
                                        session_id='admin', history=freeaiAPI.history, function_modules=function_modules,
                                        sysText=sysText, reqText=reqText, inpText=inpText, filePath=filePath,
                                        inpLang='ja', outLang='ja', )
                print()
                print(f"[{ res_name }] ({ res_api })")
                print(str(res_text))
                print()

            if False:
                sysText = None
                reqText = ''
                inpText = '兵庫県三木市の天気？'
                print()
                print('[Request]')
                print(reqText, inpText )
                print()
                res_text, res_path, res_files, res_name, res_api, freeaiAPI.history = \
                    freeaiAPI.chatBot(  chat_class='auto', model_select='auto', 
                                        session_id='admin', history=freeaiAPI.history, function_modules=function_modules,
                                        sysText=sysText, reqText=reqText, inpText=inpText, filePath=filePath,
                                        inpLang='ja', outLang='ja', )
                print()
                print(f"[{ res_name }] ({ res_api })")
                print(str(res_text))
                print()

            if False:
                sysText = None
                reqText = ''
                inpText = 'この画像はなんだと思いますか？'
                filePath = ['_icons/dog.jpg', '_icons/kyoto.png']
                print()
                print('[Request]')
                print(reqText, inpText )
                print()
                res_text, res_path, res_files, res_name, res_api, freeaiAPI.history = \
                    freeaiAPI.chatBot(  chat_class='auto', model_select='auto', 
                                        session_id='admin', history=freeaiAPI.history, function_modules=function_modules,
                                        sysText=sysText, reqText=reqText, inpText=inpText, filePath=filePath,
                                        inpLang='ja', outLang='ja', )
                print()
                print(f"[{ res_name }] ({ res_api })")
                print(str(res_text))
                print()

            if False:
                print('[History]')
                for h in range(len(freeaiAPI.history)):
                    print(freeaiAPI.history[h])
                freeaiAPI.history = []



