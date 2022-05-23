# janken ver.6.6

import tkinter as tk
from tkinter import ttk
import random as rd
import time


class Janken_game(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.master.title('じゃんけんゲーム')
        self.master.minsize(400, 400)
        startbutton = tk.Button(text='スタート')
        startbutton.place(x=175, y=300)
        startbutton['command'] = self.create_gamegamen
        self.label = tk.Label(text='じゃんけんゲームへようこそ!')
        self.label.place(x=135, y=30)
        self.label = tk.Label(text='じゃんけんに勝つと相手にダメージを与えられ、先に相手の体力を0にした方が勝ちです!')
        self.label.place(x=1, y=65)
        self.label2 = tk.Label(text='メニューからキャラと魔法を選んでスタートボタンを押すと開始します!')
        self.label2.place(x=50, y=85)
        self.roundcounter = 0
        self.p_point = 0
        self.e_point = 0

        # ゲーム画面のキャラ情報の高さを一括で変更可能
        self.chara_pt_y = 70
        # 各ターンの勝敗、自分と相手の手を表示する高さを一括で変更可能
        self.win_lose_y = 200
        # 魔法テキストの高さを一括で変更可能
        self.mahou_y = 227

        '''新規にキャラを作る場合はこちらの登録1と登録2を済ませること'''
        # キャラ情報の登録1(任意にセルフ変数を決め、そこにグー、チョキ、パー、体力、キャラ名の順に並べたリストを紐付ける)
        # グーチョキパーの重み付けを追加、リストの6、7、8番目はそれぞれグーチョキパーの出る確率(隠しステータス)
        self.luck = [2, 2, 2, 20, 'ラック', 1, 1, 1]
        self.rock = [3, 2, 1, 20, 'ロック', 1, 1, 1]
        self.scissors = [1, 3, 2, 20, 'シザー', 1, 1, 1]
        self.paper = [2, 1, 3, 20, 'ペーパ', 1, 1, 1]
        self.ishio = [3, 1, 1, 25, 'いしお', 1, 2, 1]
        self.hasami = [1, 3, 1, 25, 'はさみ', 1, 1, 2]
        self.kamiko = [1, 1, 3, 25, 'かみこ', 2, 1, 1]

        # キャラ情報の登録2(キャラ名をキー、登録1で決めたセルフ変数をバリューとして辞書に登録)
        self.chara_dict = {'ラック': self.luck, 'ロック': self.rock, 'シザー': self.scissors, 'ペーパ': self.paper, \
                           'いしお': self.ishio, 'はさみ': self.hasami, 'かみこ': self.kamiko}
        self.charanum = len(self.chara_dict) - 1

        '''魔法の登録'''
        # 魔法名をキーに、効果の説明をバリューとして辞書に登録
        self.mahou_dict = {'火炎の魔法':'3ターンの間相手の体力を少しずつ減らします',\
                           '回復の魔法':'3ターンの間自分の体力を少しずつ回復します',\
                           '強化の魔法':'5ターンの間自分の一番弱い手を強化します',
                           '封印の魔法':'3ターンの間相手の一番強い手を封じます'}

        self.mahounum = len(self.mahou_dict) - 1

        self.create_combobox()
        self.master.mainloop()


    # ウィンドウの作成メソッド
    def create_window(self):
        self.master = tk.Tk()
        self.master.title('じゃんけんゲーム')
        self.master.minsize(400, 400)

    # ウィンドウの削除メソッド
    def delete_window(self):
        self.master.destroy()

    # 体力ゲージの表示メソッド
    def hp_graph(self):
        self.label6 = tk.Label(text='残り体力:' + str(self.p_chara_hp) + 'pt  ')
        self.label6.place(x=10, y=263)
        self.label7 = tk.Label(text='残り体力:' + str(self.e_chara_hp) + 'pt  ')
        self.label7.place(x=312, y=263)

        canvas = tk.Canvas(self.master, width=30, height=150)
        canvas2 = tk.Canvas(self.master, width=30, height=150)

        # 体力が異なるキャラ同士でも体力ゲージの減り具合が均一になるように補正
        adjust_adjust = 20 / self.p_chara[3]
        adjust_adjust2 = 20 / self.e_chara[3]
        # 体力ゲージの減り具合を一括で調節する変数
        graph_adjust = 7.0 * adjust_adjust
        graph_adjust2 = 7.0 * adjust_adjust2

        # 残り体力によってゲージの色が変わるように書き分け
        if self.p_chara_hp / self.p_chara[3] > 1 / 2:
            canvas.create_rectangle(5, (2 + (self.p_chara[3] - self.p_chara_hp)) * graph_adjust, 30, 150, fill='SeaGreen3')
            canvas.place(x=30, y=105)
        elif 1 / 2 >= self.p_chara_hp / self.p_chara[3] > 1 / 4:
            canvas.create_rectangle(5, (2 + (self.p_chara[3] - self.p_chara_hp)) * graph_adjust, 30, 150, fill='yellow3')
            canvas.place(x=30, y=105)
        else:
            canvas.create_rectangle(5, (2 + (self.p_chara[3] - self.p_chara_hp)) * graph_adjust, 30, 150, fill='red3')
            canvas.place(x=30, y=105)

        if self.e_chara_hp / self.e_chara[3] > 1 / 2:
            canvas2.create_rectangle(5, (2 + (self.e_chara[3] - self.e_chara_hp)) * graph_adjust2, 30, 150, fill='SeaGreen3')
            canvas2.place(x=340, y=105)
        elif 1 / 2 >= self.e_chara_hp / self.e_chara[3] > 1 / 4:
            canvas2.create_rectangle(5, (2 + (self.e_chara[3] - self.e_chara_hp)) * graph_adjust2, 30, 150, fill='yellow3')
            canvas2.place(x=340, y=105)
        else:
            canvas2.create_rectangle(5, (2 + (self.e_chara[3] - self.e_chara_hp)) * graph_adjust2, 30, 150, fill='red3')
            canvas2.place(x=340, y=105)


    # キャラ選択画面の作成メソッド
    def create_combobox(self):
        self.charalist = list(self.chara_dict.keys())
        self.select = ttk.Combobox(master=self.master, state='readonly', values=self.charalist)
        self.select.place(x=124, y=180)

        self.label9 = tk.Label(text='キャラと魔法を選択')
        self.label9.place(x=150, y=157)

        self.infobutton = tk.Button(text='キャラの能力を見る')
        self.infobutton['command'] = self.chara_info
        self.infobutton.place(x=270, y=177)

        self.mahoulist = list(self.mahou_dict.keys())
        self.select2 = ttk.Combobox(master=self.master, state='readonly', values=self.mahoulist)
        self.select2.place(x=124, y=240)

        self.infobutton = tk.Button(text='魔法の効果を見る')
        self.infobutton['command'] = self.mahou_info
        self.infobutton.place(x=270, y=237)


        self.select.current(0)
        self.select2.current(0)

    # キャラの説明を表示するメソッド
    def chara_info(self):
        self.charaname = self.select.get()
        self.charainfo = self.chara_dict[self.charaname]
        self.label10 = tk.Label(text='体力:' + str(self.charainfo[3]) + 'pt グー:' + str(self.charainfo[0]) +
                                      'pt チョキ:' + str(self.charainfo[1]) + 'pt パー:' + str(self.charainfo[2]) + 'pt')
        self.label10.place(x=104, y=203)

    # 魔法の説明を表示するメソッド
    def mahou_info(self):
        self.mahouname = self.select2.get()
        self.mahouinfo = self.mahou_dict[self.mahouname]
        self.label16 = tk.Label(text=self.mahouinfo)
        self.label16.place(x=95, y=263)

    # スタート画面の作成メソッド
    def create_shokigamen(self):
        self.delete_window()
        self.create_window()
        self.p_point = 0
        self.e_point = 0
        startbutton = tk.Button(text='スタート')
        startbutton.place(x=175, y=300)
        startbutton['command'] = self.create_gamegamen
        self.label = tk.Label(text='じゃんけんゲームへようこそ!')
        self.label.place(x=135, y=30)
        self.label = tk.Label(text='じゃんけんに勝つと相手にダメージを与えられ、先に相手の体力を0にした方が勝ちです!')
        self.label.place(x=1, y=65)
        self.label2 = tk.Label(text='メニューからキャラを選んでスタートボタンを押すと開始します!')
        self.label2.place(x=57, y=85)
        self.create_combobox()
        self.select.current(0)

        self.master.mainloop()

    # リザルト画面の作成メソッド
    def create_resultgamen(self):
        self.delete_window()
        self.create_window()

        self.kekka = '         　　    ggs!       　　      '
        if self.p_chara_hp > 0:
            self.label8 = tk.Label(text='　勝ち!　')
            self.label8.place(x=169, y=80)
        else:
            self.label8 = tk.Label(text='　負け!　')
            self.label8.place(x=169, y=80)

        if self.p_chara_hp / self.p_chara[3] >= 3/4:
            self.kekka = '    圧勝ですね!    '
        elif 3/4 > self.p_chara_hp / self.p_chara[3] >= 1/4:
            self.kekka = '　 ナイスウィン!  　'
        elif 1/4 > self.p_chara_hp / self.p_chara[3] > 0:
            self.kekka = '   接戦でしたね!   '
        elif 1/4 > self.e_chara_hp / self.e_chara[3] > 0 :
            self.kekka = ' 惜しかったですね!  '
        elif 3/4 > self.e_chara_hp / self.e_chara[3] >= 1/4:
            self.kekka = ' きつそうでしたね... '
        elif self.p_chara_hp / self.p_chara[3] >= 3/4:
            self.kekka = '   完敗でしたね...   '

        self.label8 = tk.Label(text=self.kekka)
        self.label8.place(x=148, y=100)

        self.backbutton = tk.Button(text='スタート画面に戻る')
        self.backbutton['command'] = self.create_shokigamen
        self.backbutton.place(x=148, y=300)


    # 自分と相手のキャラを調整、確定するメソッド
    def chara_set(self):
        self.chara = self.select.get()
        self.p_chara = self.chara_dict[self.chara]

        enemynum = rd.randint(0, self.charanum)
        self.enemy = self.charalist[enemynum]
        self.e_chara = self.chara_dict[self.enemy]

        self.p_chara_hp = self.p_chara[3]
        self.e_chara_hp = self.e_chara[3]

        self.weight_list = list(self.e_chara[5:8])

        # こちらのキャラの攻撃力に応じて相手キャラの選好を変化させる
        # こちらのキャラの攻撃力がすべて同じ場合はこの調整はスキップ
        self.p_chara_max = self.p_chara[0:3].index(max(self.p_chara[0:3]))
        self.e_chara_max = self.e_chara[0:3].index(max(self.e_chara[0:3]))
        self.p_chara_min = self.p_chara[0:3].index(min(self.p_chara[0:3]))
        self.e_chara_min = self.e_chara[0:3].index(min(self.e_chara[0:3]))
        if self.p_chara[0] == self.p_chara[1] == self.p_chara[2]:
            pass
        else:
            if self.p_chara_max == 0:
                self.weight_list[1] *= 2/3
            elif self.p_chara_max == 1:
                self.weight_list[2] *= 2/3
            else:
                self.weight_list[0] *= 2/3

        self.p_mahou = self.select2.get()
        mahounum = rd.randint(0, self.mahounum)
        self.e_mahou = self.mahoulist[mahounum]
        self.p_mahou_state = 0
        self.e_mahou_state = 0
        self.e_mahou_power = 1
        self.e_mahou_time = 3/4 #相手が魔法を発動するタイミング
        self.p_mahoucounter = 0
        self.e_mahoucounter = 0
        self.p_mahou_flag = 0
        self.e_mahou_flag = 0
        self.e_mahou_text_state = 1
        self.G_huuin = 0
        self.C_huuin = 0
        self.P_huuin = 0

    # ゲーム画面の作成メソッド
    def create_gamegamen(self):
        self.chara_set()
        self.delete_window()
        self.create_window()
        self.G_button = tk.Button(text='グー', command=self.janken_G)
        self.C_button = tk.Button(text='チョキ', command=self.janken_C)
        self.P_button = tk.Button(text='パー', command=self.janken_P)
        self.M_button = tk.Button(text=self.p_mahou, command=self.janken_M)
        self.G_button.place(x=145, y=320)
        self.C_button.place(x=176, y=320)
        self.P_button.place(x=215, y=320)
        self.M_button.place(x=160, y=290)
        self.round_label = tk.Label(text='round1', font=('', 12))
        self.round_label.place(x=170, y=50)

        self.label = tk.Label(text='出す手を選択してください!')
        self.label.place(x=131, y=355)
        self.label11 = tk.Label(text='あなたのキャラ:' + str(self.chara))
        self.label11.place(x=10, y=210+self.chara_pt_y)
        self.show_p_status()

        self.label11 = tk.Label(text='相手のキャラ:' + str(self.enemy))
        self.label11.place(x=297, y=210+self.chara_pt_y)
        self.show_e_status()

        self.hp_graph()

        self.master.mainloop()

    # グーを出したときの動作メソッド
    def janken_G(self):
        self.hp_graph()
        self.e_GCP()
        self.label3 = tk.Label(text=f'あなた: グー　　相手:{self.e_hand}', font=('', 11))
        self.label3.place(x=110, y=self.win_lose_y-70)

        win_damage = self.p_chara[0]
        lose_damage = self.e_chara[2]

        if self.e_hand == 'グー  ':
            self.drow()
        elif self.e_hand == 'チョキ':
            self.win(win_damage)
        else:
            self.lose(lose_damage)

        self.hp_graph()
        self.count()
        self.master.mainloop()

    # チョキを出したときの動作メソッド
    def janken_C(self):
        self.hp_graph()
        self.e_GCP()

        self.label3 = tk.Label(text=f'あなた: チョキ 　相手:{self.e_hand}', font=('', 11))
        self.label3.place(x=110, y=self.win_lose_y-70)

        win_damage = self.p_chara[1]
        lose_damage = self.e_chara[0]

        if self.e_hand == 'グー  ':
            self.lose(lose_damage)
        elif self.e_hand == 'チョキ':
            self.drow()
        else:
            self.win(win_damage)

        self.hp_graph()
        self.count()
        self.master.mainloop()

    # パーを出したときの動作メソッド
    def janken_P(self):
        self.hp_graph()
        self.e_GCP()

        self.label3 = tk.Label(text=f'あなた: パー　　相手:{self.e_hand}', font=('', 11))
        self.label3.place(x=110, y=self.win_lose_y-70)

        win_damage = self.p_chara[2]
        lose_damage = self.e_chara[1]

        if self.e_hand == 'グー  ':
            self.win(win_damage)
        elif self.e_hand == 'チョキ':
            self.lose(lose_damage)
        else:
            self.drow()

        self.hp_graph()
        self.count()
        self.master.mainloop()

    # 相手の手を決めるメソッド
    def e_GCP(self):
        if self.G_huuin == 1:
            self.e_hand = rd.choice(['チョキ', 'パー  '])
        elif self.C_huuin == 1:
            self.e_hand = rd.choice(['グー　', 'パー  '])
        elif self.P_huuin == 1:
            self.e_hand = rd.choice(['グー　', 'チョキ'])
        else:
            e_hand_pre = rd.choices(['グー  ', 'チョキ', 'パー  '], weights=(self.weight_list))
            self.e_hand = e_hand_pre[0]

    # 魔法ボタンを押したときの処理メソッド
    def janken_M(self):
        if self.p_mahou == '回復の魔法' and self.p_chara_hp == self.p_chara[3]:
            self.hp_full_label = tk.Label(text='体力が満タンです!')
            self.hp_full_label.place(x=145, y=self.mahou_y)
            self.master.update_idletasks()
            time.sleep(2)
            self.hp_full_label['text'] = '　　　　　　　　　 　　　　　'
        else:
            self.M_button['state'] = 'disable'
            self.label = self.label17 = tk.Label(text=str(self.p_mahou) + 'を使った!', fg='blue4')
            self.label17.place(x=145, y=self.mahou_y)
            self.label = self.p_mahou_label = tk.Label(text=str(self.p_mahou) + 'を発動中!', fg='blue4')
            self.p_mahou_label.place(x=8, y=345)
            self.delete_mahou_text()
            self.p_mahou_state = 1
            self.p_mahou_flag = 1

    # 各種カウンターのカウントメソッド
    def count(self):
        self.roundcounter += 1
        self.round_label['text'] = 'round' + str(self.roundcounter)
        if self.e_chara_hp <= self.e_chara[3] * self.e_mahou_time and self.e_mahou_power == 1:
            self.e_mahou_power = 0
            self.e_mahou_state = 1
            self.e_mahou_process()
        if self.e_mahou_state == 1:
            self.e_mahou_process()

        self.p_mahou_process()

        # どちらかの体力が0になったらゲーム画面を閉じリザルト画面に移行する
        if self.p_chara_hp <= 0 or self.e_chara_hp <= 0:
            self.create_resultgamen()


    # 毎ターンの魔法の処理メソッド
    def p_mahou_process(self):
        if self.p_mahou_state == 1:
            if self.p_mahou == '火炎の魔法':
                self.e_chara_hp -= 1
                self.p_mahoucounter += 1
                self.label18 = tk.Label(text='火炎の魔法で1ダメージ与えた!', fg='blue4')
                self.label18.place(x=125, y=self.mahou_y)
                self.delete_mahou_text()
                if self.p_mahoucounter > 3:
                    self.p_mahou_end()

            elif self.p_mahou == '回復の魔法':
                self.p_chara_hp += 1
                self.p_mahoucounter += 1
                self.label17 = tk.Label(text='回復の魔法で体力を1回復した!', fg='blue4')
                self.label17.place(x=125, y=self.mahou_y)
                self.delete_mahou_text()
                if self.p_mahoucounter > 3:
                    self.p_mahou_end()

            elif self.p_mahou == '強化の魔法':
                if self.p_mahou_flag == 1:
                    self.p_chara[self.p_chara_min] *= 3

                    if self.p_chara_min == 0:
                        self.p_G_label['fg'] = 'blue4'
                        self.p_G_label['text'] = 'グー:' + str(self.p_chara[0]) + 'pt　'
                    elif self.p_chara_min == 1:
                        self.p_C_label['fg'] = 'blue4'
                        self.p_C_label['text'] = 'チョキ:' + str(self.p_chara[1]) + 'pt　'
                    elif self.p_chara_min == 2:
                        self.p_P_label['fg'] = 'blue4'
                        self.p_P_label['text'] = 'パー:' + str(self.p_chara[2]) + 'pt　'

                    self.p_mahou_flag = 0

                self.p_mahoucounter += 1
                if self.p_mahoucounter > 5:
                    self.p_chara[self.p_chara_min] = int(self.p_chara[self.p_chara_min] / 3)
                    self.show_p_status()
                    self.p_mahou_end()

            elif self.p_mahou == '封印の魔法':
                if self.e_chara_max == 0:
                    self.G_huuin = 1
                    self.e_G_label['font'] = ('', 9, 'overstrike')
                elif self.e_chara_max == 1:
                    self.C_huuin = 1
                    self.e_C_label['font'] = ('', 9, 'overstrike')
                elif self.e_chara_max == 2:
                    self.P_huuin = 1
                    self.e_P_label['font'] = ('', 9, 'overstrike')
                self.p_mahoucounter += 1

                if self.p_mahoucounter > 3:
                    self.G_huuin = 0
                    self.C_huuin = 0
                    self.P_huuin = 0
                    self.show_e_status()
                    self.p_mahou_end()

        else:
            pass


    # 相手側の魔法処理メソッド
    def e_mahou_process(self):
        if self.e_mahou_state == 1:
            if self.e_mahou_text_state == 1:
                self.label = self.label17 = tk.Label(text='相手は' + str(self.e_mahou) + 'を使った!', fg='red4')
                self.label17.place(x=130, y=self.mahou_y)
                self.label = self.label17 = tk.Label(text=str(self.e_mahou) + 'を発動中!', fg='red4')
                self.label17.place(x=287, y=345)
                self.delete_mahou_text()
                self.e_mahou_flag = 1
                self.e_mahou_text_state = 0

            if self.e_mahou == '火炎の魔法':
                self.p_chara_hp -= 1
                self.e_mahoucounter += 1
                self.label17 = tk.Label(text='相手の火炎の魔法で1ダメージ受けた!', fg='red4')
                self.label17.place(x=105, y=self.mahou_y)
                self.delete_mahou_text()
                if self.e_mahoucounter > 3:
                    self.e_mahou_end()

            elif self.e_mahou == '回復の魔法':
                self.e_chara_hp += 1
                self.e_mahoucounter += 1
                self.label17 = tk.Label(text='相手は回復の魔法で体力を1回復した!', fg='red4')
                self.label17.place(x=105, y=self.mahou_y)
                self.delete_mahou_text()
                if self.e_mahoucounter > 3:
                    self.e_mahou_end()

            elif self.e_mahou == '強化の魔法':
                if self.e_mahou_flag == 1:
                    self.e_chara[self.e_chara_min] *= 3
                    self.e_mahou_flag = 0

                    if self.e_chara_min == 0:
                        self.e_G_label['fg'] = 'red4'
                        self.e_G_label['text'] = 'グー:' + str(self.e_chara[0]) + 'pt　'
                    elif self.e_chara_min == 1:
                        self.e_C_label['fg'] = 'red4'
                        self.e_G_label['text'] = 'チョキ:' + str(self.e_chara[1]) + 'pt　'
                    elif self.e_chara_min == 2:
                        self.e_P_label['fg'] = 'red4'
                        self.e_G_label['text'] = 'パー:' + str(self.e_chara[2]) + 'pt　'

                self.e_mahoucounter += 1
                if self.e_mahoucounter > 5:
                    self.e_chara[self.e_chara_min] = int(self.e_chara[self.e_chara_min] / 3)
                    self.show_e_status()
                    self.e_mahou_end()

            elif self.e_mahou == '封印の魔法':
                if self.p_chara_max == 0:
                    self.G_button['state'] = 'disable'
                    self.p_G_label['font'] = ('', 9, 'overstrike')
                elif self.p_chara_max == 1:
                    self.C_button['state'] = 'disable'
                    self.p_C_label['font'] = ('', 9, 'overstrike')
                elif self.p_chara_max == 2:
                    self.P_button['state'] = 'disable'
                    self.p_P_label['font'] = ('', 9, 'overstrike')

                self.e_mahoucounter += 1

                if self.e_mahoucounter > 3:
                    self.G_button['state'] = 'normal'
                    self.C_button['state'] = 'normal'
                    self.P_button['state'] = 'normal'
                    self.show_p_status()
                    self.e_mahou_end()

        else:
            pass

    #魔法のテキストを任意の秒数表示して削除するメソッド
    def delete_mahou_text(self):
        self.G_button['state'] = 'disable'
        self.C_button['state'] = 'disable'
        self.P_button['state'] = 'disable'
        self.master.update_idletasks()
        time.sleep(1)
        self.G_button['state'] = 'normal'
        self.C_button['state'] = 'normal'
        self.P_button['state'] = 'normal'
        self.label = self.label19 = tk.Label(text='　　　　　 　　　　　 　 　　　　　　　')
        self.label19.place(x=100, y=self.mahou_y)

    #魔法を終了するメソッド
    def p_mahou_end(self):
        self.label = self.label17 = tk.Label(text=str(self.p_mahou) + 'の効果が切れた!　　')
        self.label17.place(x=127, y=self.mahou_y)
        self.delete_mahou_text()
        self.p_mahou_state = 0
        self.label18 = tk.Label(text='　　　　　　　　　')
        self.label18.place(x=5, y=345)

    #相手の魔法を終了するメソッド
    def e_mahou_end(self):
        self.label = self.label17 = tk.Label(text='相手の' + str(self.e_mahou) + 'の効果が切れた!　　')
        self.label17.place(x=108, y=self.mahou_y)
        self.delete_mahou_text()
        self.e_mahou_state = 0
        self.label18 = tk.Label(text='　　　　　　　　　')
        self.label18.place(x=285, y=345)

    # じゃんけんに勝ったときの処理メソッド
    def win(self, win_damage):
        self.label4 = tk.Label(text='　勝ち!　　', fg='blue4', font=('', 12))
        self.label4.place(x=163, y=self.win_lose_y-25)
        self.e_chara_hp -= win_damage
        self.label15 = tk.Label(text=str(win_damage) + 'ダメージを与えた!　', fg='blue4')
        self.label15.place(x=155, y=self.win_lose_y)

    # じゃんけんに負けたときの処理メソッド
    def lose(self, lose_damage):
        self.label4 = tk.Label(text='　負け!　　', fg='red4', font=('', 12))
        self.label4.place(x=163, y=self.win_lose_y-25)
        self.p_chara_hp -= lose_damage
        self.label15 = tk.Label(text=str(lose_damage) + 'ダメージを受けた!　', fg='red4')
        self.label15.place(x=155, y=self.win_lose_y)

    # じゃんけんに引き分けたときの処理メソッド
    def drow(self):
        self.label4 = tk.Label(text='引き分け!', font=('', 12))
        self.label4.place(x=163, y=self.win_lose_y-25)
        self.label15 = tk.Label(text='                                       ')
        self.label15.place(x=155, y=self.win_lose_y)

    # ゲーム画面に自分のキャラのステータスを表示するメソッド
    def show_p_status(self):
        self.p_G_label = tk.Label(text='グー:' + str(self.p_chara[0]) + 'pt　')
        self.p_G_label.place(x=10, y=228 + self.chara_pt_y)
        self.p_C_label = tk.Label(text='チョキ:' + str(self.p_chara[1]) + 'pt　')
        self.p_C_label.place(x=10, y=243 + self.chara_pt_y)
        self.p_P_label = tk.Label(text='パー:' + str(self.p_chara[2]) + 'pt　')
        self.p_P_label.place(x=10, y=258 + self.chara_pt_y)

    # ゲーム画面に相手のキャラのステータスを表示するメソッド
    def show_e_status(self):
        self.e_G_label = tk.Label(text='グー:' + str(self.e_chara[0]) + 'pt　')
        self.e_G_label.place(x=345, y=228 + self.chara_pt_y)
        self.e_C_label = tk.Label(text='チョキ:' + str(self.e_chara[1]) + 'pt　')
        self.e_C_label.place(x=338, y=243 + self.chara_pt_y)
        self.e_P_label = tk.Label(text='パー:' + str(self.e_chara[2]) + 'pt　')
        self.e_P_label.place(x=345, y=258 + self.chara_pt_y)


# ゲームの実行コマンド
def main():
    win = tk.Tk()
    app = Janken_game(master=win)
    app.mainloop()


if __name__ =='__main__':
    main()
