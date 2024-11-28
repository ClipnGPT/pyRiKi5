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

# perplexity チャットボット
import openai

import speech_bot_perplexity_key  as perplexity_key



# base64 encode
def base64_encode(file_path):
    with open(file_path, "rb") as input_file:
        return base64.b64encode(input_file.read()).decode('utf-8')



class _perplexityAPI:

    def __init__(self, ):
        self.log_queue                  = None
        self.bot_auth                   = None

        self.temperature                = 0.8
        self.timeOut                    = 60

        self.perplexity_api_type        = 'perplexity'
        self.perplexity_default_gpt     = 'auto'
        self.perplexity_default_class   = 'auto'
        self.perplexity_auto_continue   = 3
        self.perplexity_max_step        = 10
        self.perplexity_max_session     = 5
       
        self.perplexity_key_id          = None

        self.perplexity_a_enable        = False
        self.perplexity_a_nick_name     = ''
        self.perplexity_a_model         = None
        self.perplexity_a_token         = 0

        self.perplexity_b_enable        = False
        self.perplexity_b_nick_name     = ''
        self.perplexity_b_model         = None
        self.perplexity_b_token         = 0

        self.perplexity_v_enable        = False
        self.perplexity_v_nick_name     = ''
        self.perplexity_v_model         = None
        self.perplexity_v_token         = 0

        self.perplexity_x_enable        = False
        self.perplexity_x_nick_name     = ''
        self.perplexity_x_model         = None
        self.perplexity_x_token         = 0

        self.history                    = []

        self.seq                        = 0
        self.reset()

    def init(self, log_queue=None, ):
        self.log_queue = log_queue
        return True

    def reset(self, ):
        self.history                    = []
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
                     perplexity_api_type,
                     perplexity_default_gpt, perplexity_default_class,
                     perplexity_auto_continue,
                     perplexity_max_step, perplexity_max_session,

                     perplexity_key_id,

                     perplexity_a_nick_name, perplexity_a_model, perplexity_a_token, 
                     perplexity_b_nick_name, perplexity_b_model, perplexity_b_token, 
                     perplexity_v_nick_name, perplexity_v_model, perplexity_v_token, 
                     perplexity_x_nick_name, perplexity_x_model, perplexity_x_token, 
                    ):

        # 設定

        # 認証
        self.bot_auth                       = None
        self.perplexity_key_id              = perplexity_key_id

        self.perplexity_default_gpt         = perplexity_default_gpt
        self.perplexity_default_class       = perplexity_default_class
        if (str(perplexity_auto_continue) != 'auto'):
            self.perplexity_auto_continue   = int(perplexity_auto_continue)
        if (str(perplexity_max_step)      != 'auto'):
            self.perplexity_max_step        = int(perplexity_max_step)
        if (str(perplexity_max_session) != 'auto'):
            self.perplexity_max_session     = int(perplexity_max_session)

        # perplexity チャットボット
        if (perplexity_a_nick_name != ''):
            self.perplexity_a_enable        = False
            self.perplexity_a_nick_name     = perplexity_a_nick_name
            self.perplexity_a_model         = perplexity_a_model
            self.perplexity_a_token         = int(perplexity_a_token)

        if (perplexity_b_nick_name != ''):
            self.perplexity_b_enable        = False
            self.perplexity_b_nick_name     = perplexity_b_nick_name
            self.perplexity_b_model         = perplexity_b_model
            self.perplexity_b_token         = int(perplexity_b_token)

        if (perplexity_v_nick_name != ''):
            self.perplexity_v_enable        = False
            self.perplexity_v_nick_name     = perplexity_v_nick_name
            self.perplexity_v_model         = perplexity_v_model
            self.perplexity_v_token         = int(perplexity_v_token)

        if (perplexity_x_nick_name != ''):
            self.perplexity_x_enable        = False
            self.perplexity_x_nick_name     = perplexity_x_nick_name
            self.perplexity_x_model         = perplexity_x_model
            self.perplexity_x_token         = int(perplexity_x_token)

        # API-KEYの設定
        self.client = None
        if (perplexity_key_id[:1] == '<'):
            return False
        try:
            self.client = openai.OpenAI(
                api_key=perplexity_key_id,
                base_url="https://api.perplexity.ai",
            )
        except Exception as e:
            print(e)
            return False

        # モデル
        hit = False
        if (self.perplexity_a_model != ''):
            self.perplexity_a_enable = True
            hit = True
        if (self.perplexity_b_model != ''):
            self.perplexity_b_enable = True
            hit = True
        if (self.perplexity_v_model != ''):
            self.perplexity_v_enable = True
            hit = True
        if (self.perplexity_x_model != ''):
            self.perplexity_x_enable = True
            hit = True

        if (hit == True):
            self.bot_auth = True
            return True
        else:
            return False

    def setTimeOut(self, timeOut=60, ):
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

    def history2msg_pplx(self, history=[], ):
        # 過去メッセージ追加
        msg_text = ''
        if (len(history) > 1):
            msg_text += "''' これは過去の会話履歴です。\n"
            for m in range(len(history) - 1):
                role    = history[m].get('role','')
                content = history[m].get('content','')
                name    = history[m].get('name','')
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

        res_msg = []
        dic = {'role': 'user', 'content': msg_text }
        res_msg.append(dic)

        return res_msg



    def files_check(self, filePath=[], ):
        upload_files = []
        image_urls   = []

        # filePath確認
        if (len(filePath) > 0):
            try:

                for file_name in filePath:
                    if (os.path.isfile(file_name)):
                        # 2024/06/26 時点 max 10Mbyte 
                        if (os.path.getsize(file_name) <= 10000000):

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
            self.print(session_id, ' perplexity  : Not Authenticate Error !')
            return res_text, res_path, res_name, res_api, res_history

        # モデル 設定
        res_name = self.perplexity_a_nick_name
        res_api  = self.perplexity_a_model
        if  (chat_class == 'perplexity'):
            if (self.perplexity_b_enable == True):
                res_name = self.perplexity_b_nick_name
                res_api  = self.perplexity_b_model
        if  (chat_class == 'pplx'):
            if (self.perplexity_x_enable == True):
                res_name = self.perplexity_x_nick_name
                res_api  = self.perplexity_x_model

        # モデル 補正 (assistant)
        if ((chat_class == 'assistant') \
        or  (chat_class == 'コード生成') \
        or  (chat_class == 'コード実行') \
        or  (chat_class == '文書検索') \
        or  (chat_class == '複雑な会話') \
        or  (chat_class == 'アシスタント') \
        or  (model_select == 'x')):
            if (self.perplexity_x_enable == True):
                res_name = self.perplexity_x_nick_name
                res_api  = self.perplexity_x_model

        # model 指定
        if (self.perplexity_a_nick_name != ''):
            if (inpText.strip()[:len(self.perplexity_a_nick_name)+1].lower() == (self.perplexity_a_nick_name.lower() + ',')):
                inpText = inpText.strip()[len(self.perplexity_a_nick_name)+1:]
        if (self.perplexity_b_nick_name != ''):
            if (inpText.strip()[:len(self.perplexity_b_nick_name)+1].lower() == (self.perplexity_b_nick_name.lower() + ',')):
                inpText = inpText.strip()[len(self.perplexity_b_nick_name)+1:]
                if   (self.perplexity_b_enable == True):
                        res_name = self.perplexity_b_nick_name
                        res_api  = self.perplexity_b_model
        if (self.perplexity_v_nick_name != ''):
            if (inpText.strip()[:len(self.perplexity_v_nick_name)+1].lower() == (self.perplexity_v_nick_name.lower() + ',')):
                inpText = inpText.strip()[len(self.perplexity_v_nick_name)+1:]
                if   (self.perplexity_v_enable == True):
                    if  (len(image_urls) > 0) \
                    and (len(image_urls) == len(upload_files)):
                        res_name = self.perplexity_v_nick_name
                        res_api  = self.perplexity_v_model
                elif (self.perplexity_x_enable == True):
                        res_name = self.perplexity_x_nick_name
                        res_api  = self.perplexity_x_model
        if (self.perplexity_x_nick_name != ''):
            if (inpText.strip()[:len(self.perplexity_x_nick_name)+1].lower() == (self.perplexity_x_nick_name.lower() + ',')):
                inpText = inpText.strip()[len(self.perplexity_x_nick_name)+1:]
                if   (self.perplexity_x_enable == True):
                        res_name = self.perplexity_x_nick_name
                        res_api  = self.perplexity_x_model
                elif (self.perplexity_b_enable == True):
                        res_name = self.perplexity_b_nick_name
                        res_api  = self.perplexity_b_model
        if   (inpText.strip()[:5].lower() == ('riki,')):
            inpText = inpText.strip()[5:]
            if   (self.perplexity_x_enable == True):
                        res_name = self.perplexity_x_nick_name
                        res_api  = self.perplexity_x_model
            elif (self.perplexity_b_enable == True):
                        res_name = self.perplexity_b_nick_name
                        res_api  = self.perplexity_b_model
        elif (inpText.strip()[:7].lower() == ('vision,')):
            inpText = inpText.strip()[7:]
            if   (self.perplexity_v_enable == True):
                if  (len(image_urls) > 0) \
                and (len(image_urls) == len(upload_files)):
                        res_name = self.perplexity_v_nick_name
                        res_api  = self.perplexity_v_model
            elif (self.perplexity_x_enable == True):
                        res_name = self.perplexity_x_nick_name
                        res_api  = self.perplexity_x_model
        elif (inpText.strip()[:10].lower() == ('assistant,')):
            inpText = inpText.strip()[10:]
            if (self.perplexity_b_enable == True):
                        res_name = self.perplexity_b_nick_name
                        res_api  = self.perplexity_b_model
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
            res_name = self.perplexity_a_nick_name
            res_api  = self.perplexity_a_model
            if (self.perplexity_b_enable == True):
                if (len(upload_files) > 0) \
                or (len(inpText) > 1000):
                    res_name = self.perplexity_b_nick_name
                    res_api  = self.perplexity_b_model

        # モデル 補正 (vision)
        if  (len(image_urls) > 0) \
        and (len(image_urls) == len(upload_files)):
            if   (self.perplexity_v_enable == True):
                res_name = self.perplexity_v_nick_name
                res_api  = self.perplexity_v_model
            elif (self.perplexity_x_enable == True):
                res_name = self.perplexity_x_nick_name
                res_api  = self.perplexity_x_model

        # history 追加・圧縮 (古いメッセージ)
        res_history = self.history_add(history=res_history, sysText=sysText, reqText=reqText, inpText=inpText, )
        res_history = self.history_zip1(history=res_history, )

        # メッセージ作成
        msg = self.history2msg_pplx(history=res_history, )

        # ストリーム実行?
        if (session_id == 'admin'):
            stream = True
        else:
            stream = False
        #print(' stream = False, ')
        #stream = False

        # 実行ループ
        #try:
        if True:

            n = 0
            function_name = ''
            while (function_name != 'exit') and (n < int(max_step)):

                # 結果
                res_role      = None
                res_content   = ''

                # GPT
                n += 1
                self.print(session_id, f" perplexity  : { res_api }, pass={ n }, ")

                # Stream 表示
                if (stream == True):
                    response = self.client.chat.completions.create(
                            model           = res_api,
                            messages        = msg,
                            temperature     = float(temperature),
                            timeout         = self.timeOut,
                            stream          = stream, 
                            )

                    chkTime     = time.time()
                    for chunk in response:
                        if ((time.time() - chkTime) > self.timeOut):
                            break
                        delta   = chunk.choices[0].delta
                        if (delta is not None):
                            if (delta.content is not None):
                                #res_role    = delta.role
                                res_role    = 'assistant'
                                content     = delta.content
                                res_content += content
                                self.stream(session_id, content)

                    # 改行
                    if (res_content != ''):
                        self.print(session_id, )


                # 通常実行
                if (stream == False):
                    response = self.client.chat.completions.create(
                            model           = res_api,
                            messages        = msg,
                            temperature     = float(temperature),
                            timeout         = self.timeOut,
                            stream          = stream, 
                            )

                    # response 処理
                    try:
                        res_role    = str(response.choices[0].message.role)
                        res_content = str(response.choices[0].message.content)
                    except:
                        pass

                # 実行終了
                function_name = 'exit'
                if (res_content.strip() != ''):
                    res_text += res_content.rstrip() + '\n'

                    self.seq += 1
                    dic = {'seq': self.seq, 'time': time.time(), 'role': 'assistant', 'name': '', 'content': res_content }
                    res_history.append(dic)

            # 正常回答
            if (res_text != ''):
                self.print(session_id, f" perplexity  : { res_name.lower() } complite.")
            else:
                self.print(session_id,  ' perplexity  : Error !')

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
            sysText = 'あなたは教師のように話す賢いアシスタントです。'

        if (self.bot_auth is None):
            self.print(session_id, ' perplexity : Not Authenticate Error !')
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

        # perplexity
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

        #perplexityAPI = speech_bot_perplexity._perplexityAPI()
        perplexityAPI = _perplexityAPI()

        api_type = perplexity_key.getkey('perplexity','perplexity_api_type')
        print(api_type)

        log_queue = queue.Queue()
        res = perplexityAPI.init(log_queue=log_queue, )

        res = perplexityAPI.authenticate('perplexity',
                            api_type,
                            perplexity_key.getkey('perplexity','perplexity_default_gpt'), perplexity_key.getkey('perplexity','perplexity_default_class'),
                            perplexity_key.getkey('perplexity','perplexity_auto_continue'),
                            perplexity_key.getkey('perplexity','perplexity_max_step'), perplexity_key.getkey('perplexity','perplexity_max_session'),
                            perplexity_key.getkey('perplexity','perplexity_key_id'),
                            perplexity_key.getkey('perplexity','perplexity_a_nick_name'), perplexity_key.getkey('perplexity','perplexity_a_model'), perplexity_key.getkey('perplexity','perplexity_a_token'),
                            perplexity_key.getkey('perplexity','perplexity_b_nick_name'), perplexity_key.getkey('perplexity','perplexity_b_model'), perplexity_key.getkey('perplexity','perplexity_b_token'),
                            perplexity_key.getkey('perplexity','perplexity_v_nick_name'), perplexity_key.getkey('perplexity','perplexity_v_model'), perplexity_key.getkey('perplexity','perplexity_v_token'),
                            perplexity_key.getkey('perplexity','perplexity_x_nick_name'), perplexity_key.getkey('perplexity','perplexity_x_model'), perplexity_key.getkey('perplexity','perplexity_x_token'),
                            )
        print('authenticate:', res, )
        if (res == True):
            
            function_modules = []
            filePath         = []

            if True:
                sysText = None
                reqText = ''
                #inpText = 'おはようございます。'
                inpText = 'soner,おはようございます。'
                print()
                print('[Request]')
                print(reqText, inpText )
                print()
                res_text, res_path, res_files, res_name, res_api, perplexityAPI.history = \
                    perplexityAPI.chatBot(  chat_class='auto', model_select='auto', 
                                            session_id='admin', history=perplexityAPI.history, function_modules=function_modules,
                                            sysText=sysText, reqText=reqText, inpText=inpText, filePath=filePath,
                                            inpLang='ja', outLang='ja', )
                print()
                print(f"[{ res_name }] ({ res_api })")
                print(str(res_text))
                print()

            if True:
                sysText = None
                reqText = ''
                #inpText = 'おはようございます。'
                #inpText = 'pplx,おはようございます。'
                inpText = 'pplx,株式会社三光システムの姫路の住所？'
                print()
                print('[Request]')
                print(reqText, inpText )
                print()
                res_text, res_path, res_files, res_name, res_api, perplexityAPI.history = \
                    perplexityAPI.chatBot(  chat_class='auto', model_select='auto', 
                                            session_id='admin', history=perplexityAPI.history, function_modules=function_modules,
                                            sysText=sysText, reqText=reqText, inpText=inpText, filePath=filePath,
                                            inpLang='ja', outLang='ja', )
                print()
                print(f"[{ res_name }] ({ res_api })")
                print(str(res_text))
                print()

            if False:
                print('[History]')
                for h in range(len(perplexityAPI.history)):
                    print(perplexityAPI.history[h])
                perplexityAPI.history = []



