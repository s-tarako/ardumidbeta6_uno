import pretty_midi
import numpy as np
import os
import sys
import json
from tkinter import filedialog 
import readchar
 #ここでset_trace()
 #Todo
    ###
    # #ファイル
    # 
    # 
    # 
    # ピッチベンド 

    # パン
    #
    # 
    #
    # ファイル指定のGUi化
    #アドオン自動生成
neirodic={"pling":"note.pling",
"harp":"note.harp",
"bass":"note.bass",
}


drumdic={'Crash Cymbal 1':("random.grass",1),
'Crash Cymbal 2':("random.grass",0.8),
'Acoustic Snare':("note.snare",0.8),
'Acoustic Bass Drum':("note.bd",1),
 'Open Hi Hat':("note.snare",2),
 'Splash Cymbal':("dig.sand",1)}
#変数
dof=False
def GenfromAPP(lst,rfn,C_name,Savelocation,IUPitchBend):
    
    #デバッグ
    def do(txt):
        if (not dof):
            print("DEBUG:",txt)

    
    

  


    

#長音処理
    def M_parse(trck,neiro,cnt,Haba,PitchBend):
        def getPB(time):
            retPB=0
            for PB_a in PitchBend:
                if(PB_a[1]<=time):
                    retPB=round(PB_a[0]/338.5)
            
            return retPB
        tmplist=list()
        tmplist2=list()
        cntA=0
        Drumlist=list()
        
        if(neiro=="drum"):
            isD=True
        else:
            isD=False
        
        for note in trck.notes:
            #ピッチ、強さ、長さ、開始チック、音色,ピッチベンド
            
            Npitch=note.pitch
            Nstart=midi_data.time_to_tick(note.start)
            Nlong=midi_data.time_to_tick(note.end-note.start)
            Nvel=note.velocity
            PBvalue=getPB(Nstart)
            tmplist.append([Npitch,Nvel,Nlong,Nstart,neiro,PBvalue])
            #print(midi_data.time_to_tick(note.end-note.start))
            cntA+=1
            if(isD):
                #print(pretty_midi.note_number_to_drum_name(note.pitch))
                if(pretty_midi.note_number_to_drum_name(note.pitch) not in Drumlist):
                    Drumlist.append(pretty_midi.note_number_to_drum_name(note.pitch))
        do("重音処理")
        for leng in tmplist:
            if(not isD):
                lenB=Bunkaino/4
                cntB=Bunkaino/4
            
                while(lenB<leng[2]):
                    PBval=getPB(leng[3]+cntB)        

                    tmplist2.append([leng[0],leng[1]-5,leng[2],leng[3]+cntB,neiro,PBval])

                    #print('long',str(leng[2]))
                    cntB+=Bunkaino/4
                    lenB+=Bunkaino/4
                
        tmplist.extend(tmplist2)
        tmplist.sort( key=lambda x: x[3])
        do(("ドラムリスト:",Drumlist))
        createC(tmplist,isD,cnt,C_name)
        
    
    def createC(note,isD,cnt,C_name):
         
         if(isD):
            for n in note:
             #ピッチ、強さ、長さ、開始チック、音色,ピッチベンド
                if(pretty_midi.note_number_to_drum_name(n[0]) in drumdic):

                    tck=int(n[3]/(Bunkaino/4))

                    Npitch=drumdic[pretty_midi.note_number_to_drum_name(n[0])][1]
                    addN(f,Npitch,tck,drumdic[pretty_midi.note_number_to_drum_name(n[0])][0],n[1])
                    if(tck>3000):
                        break
         else:
             for n in note:
             #ピッチ、強さ、長さ、開始チック、音色,ピッチベンド
             
                tck=int(n[3]/(Bunkaino/4))

                Npitch=pretty_midi.note_number_to_hz(n[0])/261.6/1.41
                addN(f,round(Npitch,3),tck,neirodic[n[4]],n[1])
                if(tck>3000):
                        break
         

    def addN(fnc,ptc,start,Neiro,vol):
        fnc.write("execute @a[tag=ensou%s,scores={note=%s}] ~~~ playsound %s @s ~~~ %s %s  \n"%(C_name,start,Neiro,str(round(vol/127,3)),ptc))
    
    do("starting Generate...") 
    midi_data = pretty_midi.PrettyMIDI(rfn)
    midi_tracks= midi_data.instruments
    Bunkaino=midi_data.resolution
    try :
        os.makedirs(Savelocation+"/"+C_name+"/")
    
    except Exception as er:
        pass
    cnt=0
    Hab=0
    f=open(Savelocation+"/"+C_name+"/main.mcfunction","w",encoding="utf8")
    f.write("""
         scoreboard objectives add note dummy "ノトブロよう"
         scoreboard players add @a[tag=ensou%s] note 1
         execute @a[tag=ensou%s,scores={note=1}] ~~~ scoreboard objectives add  dummy §a演奏開始
         
         """%(C_name,C_name))
    for trk in lst:                           
        
        do((trk[1],cnt))
        
        neiro=trk[1]
        trck=midi_tracks[cnt]
        if(trk[1]!="disable"):
            pb=trck.pitch_bends
            PitchBendlist=list()
            old=0
            for PitchBendParam in pb:

                if( midi_data.time_to_tick(PitchBendParam.time) !=old):

                    PitchBendlist.append((PitchBendParam.pitch,midi_data.time_to_tick(PitchBendParam.time)))
                old=PitchBendParam.time
            M_parse(trck,neiro,trk[0],Hab,PitchBendlist)

            cnt+=1
        else:
            do("スキップしました(Disable)")
    do("ok")


    #初期化

    


    #トラック毎処理
    
        #M_tracks(rfn,C_name)
    #if(__name__=="__main__"):

#コマンドライン処理
tm=0
try :
    if(sys.argv[1]=="getList"):
        C_name=sys.argv[2]
        midi_data = pretty_midi.PrettyMIDI(C_name)
        midi_tracks= midi_data.instruments
        
        for a in midi_tracks:
            print("%s@%s@"%(a.name,str(a.is_drum)))
except :
    a=0


try:
    
    if(sys.argv[1]=="Gf"):
        '''
        track=list()
        for a in sys.argv:
            pass

         
        fileplace=sys.argv[2]
        C_name=sys.argv[4]
        
        get=sys.argv[3][:-1].split("$")
        
        cnt=0
        for b in get:
            print(b)
        Sloc="Y:/python/mcmid/midiV3/mcfunctions"
        for word in get:
            
            
            word2=word.split("/")
            for c in word2:
               print(c," word2",)
            partname=word2[0]
            partinst=word2[1]
            partEnable=word2[2]
            print(partinst)
            track.append(partinst,partEnable)
            print(partinst,partEnable)
            for d in track:
                print(d[0],d[1]+"aaa")
            
             
        GenfromAPP(track,fileplace,C_name,Sloc)
        print('ok2')
        '''
        data=json.load(sys.argv[2])
    
        track=list()

        saveloc=sys.argv[3]
        filefrom=sys.argv[4]
        for trk in data["Trackinfo"]:
            track.append(trk["Instrument"],trk["Isenable"])
        #GenfromAPP(track,filefrom,saveloc,"Y:/python/mcmid/midiV3/mcfunctions")
    
    

except:
    a=0
    
notechar={b"p":"pling",b"h":"harp",b"g":"guitar",b"b":"bass",b"n":"disable"}
if (__name__=="__main__"):
    print("midicoreCUIif V1")
    print("ファイルを選択してください")
    fTyp = [("midi形式","*.mid")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    filepath = filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
    print(filepath,"を読み込みます...")
    midi_data = pretty_midi.PrettyMIDI(filepath)
    midi_tracks= midi_data.instruments
    print("info トラック数：%s "%len(midi_tracks))
    print("info 分解能：%s"%(midi_data.resolution))
    print("-----トラック情報-----")
    tNo=0
    for trk in midi_tracks:
        print("*トラック%s:%s"%(tNo,trk.name))
        
        tNo+=1
        

    print("保存するコマンド名を指定してください")
    
    Cn=(sys.stdin.readline()).replace("\n","")
    print(Cn)
    isok=0
    while(isok==0):

        print("トラックのステータスを指定してください")
        track=list()
        trk=0
        for t in midi_tracks:
            if(t.is_drum==True):
                print("*トラック%sはドラムです 無効化:N/有効化:D"%trk)
                while 1:

                    kb = readchar.readchar()
                    if(kb==b"d"):
                        track.append([trk,"drum"])
                        break
                    elif(kb==b"n"):
                        track.append([trk,"disable"])
                        break
                    else:
                        print("有効な文字を入力してください")
                
                
            else:   
                print("""(P:pling H:harp G:guitar B:bass N:disable)""")
                print("track%s:%s  >>"%(trk,t.name))
                    
                while 1:
                    kb = readchar.readchar()
                    if(kb in notechar):
                        print(notechar[kb])
                        track.append([trk,notechar[kb]])
                        break
                    else:
                        print("有効な文字を入力してください")
            trk+=1   
        print("トラック状況はこれでいいですか？")
        for a in track:
            print("*トラック%s:%s,音色:%s"%(a[0],midi_tracks[a[0]].name,a[1]))
        print("---------------(Y/N)")
        while 1:
                kb = readchar.readchar()
                if(kb==b"y"):
                    isok=1
                    break
                elif(kb==b"n"):
                    isok=0
                    break
                else:
                    print("有効な文字を入力してください")
                    isok=0
        print("ピッチベンドを使用しますか？(Y/N) ")
        P_IsUsePBend=False
        while 1:
                kb = readchar.readchar()
                if(kb==b"y"):
                    P_IsUsePBend=True
                    break
                elif(kb==b"n"):

                    break
                else:
                    print("有効な文字を入力してください")
                    isok=0
       
    GenfromAPP(track,filepath,Cn,"Y:/python/mcmid/midiV3/mcfunctions",P_IsUsePBend)