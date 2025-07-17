li = [1,2,3]

li_cp = li[:]

li_cp.pop(0)

print(li)




if False:

    
    # 半荘の開始
    printd("HANCHAN STARTED")
    # infoの初期化
    info.edit("kyoku", "t1")
    info.edit("hon", 0)



    while True:
        # 局の初期化
        Game = Kyoku()
        Game.reset_kyoku()
        while True:
            # プレイヤーができる操作を取得する
            capable_sousa_li = Game.get_capable_sousa()
            
            if capable_sousa_li == []: # プレイヤーの選択余地がなかったら
                cmds = None
            else:
                # プレイヤーに選択させる
                Game.dbg()
                print("capable_sousa_li:", capable_sousa_li)
                
                cmds = [input("INPUT CMD [who, sousa, hai]: ").split()]
                if cmds == [""]: cmds = None

            # プレイヤーのコマンドを実行する
            Game.do_cmds(cmds)


            # 局が終わるかの判定をここで行う
            # 誰かがアガってたら終了
            if Game.agari_data != []: 
                printd(Game.agari_data)
                break
            # 残りのツモ牌がなかったら終了
            if Game.previous_cmd == None and len(Game.YAMA) <= 4:
                # 流し満貫の判定
                # 未作成！
                break

            # ツモ進行
            Game.tumo()
        
        printd(f"FINISH {info.read()["kyoku"].upper()}")

        # 点数計算・点棒のやりとり
        oyakeep = False
        # 流局かそうでないかで場合分け
        if len(Game.agari_data) == 0: 
            printd("RYUKYOKU(?)")
            # 流し満貫の判定
            # 未作成！！！
            if False:
                Game.agari_data.append(
                    {
                        "hogehoge"
                    }
                )
        if len(Game.agari_data) != 0:
            printd("AGARI")
            # 親がキープされるかの判定
            for agd in Game.agari_data:
                if agd["whoagari"] == info.getoya():
                    oyakeep = True    
                # 点数計算・点棒移動の処理  
                # 未作成！！
        
        # 次局のためのinfo編集
        if oyakeep: # 親キープの場合
            info.edit("hon", info.read()["hon"] + 1)
        else: # 親が流れる場合
            kyoku_li = ["t1", "t2", "t3", "t4", "n1", "n2", "n3", "n4"]
            now_kyoku_index = kyoku_li.index(info.read()["kyoku"])
            if now_kyoku_index == 7: # 半荘消化終わり
                break
            else:
                info.edit("kyoku", kyoku_li[now_kyoku_index+1])
                            
        # 箱割れが発生したらbreak
        # 未作成！！！
        if False:
            break
    printd("HANCHAN FINISHED")