# TOWER-FIX-QLV-03-SELFPACK · qlv塔自演进即装包(钥到即装, 20260915T0330Z)
> 装法: TOWER_PAT值→vault(~/.keys/tower_pat.txt 600)→API contents PUT两件→验runs绿+段轮转含lanesweep/debtengine→述职销账. 全程钥值零入文.
## 件一: ci/watchtower.py 补丁(ADD1 LANE-SWEEP-01 + ADD2 DEBT-ENGINE-01)
### 补丁点A: SEG_ORDER 行(现行529)改为:
SEG_ORDER = ['keyhealth', 'secrets-meta', 'nudge', 'pulse', 'orbit', 'faces8', 'lanesweep', 'debtengine']
### 补丁点B: poll() 段族新增两段(置于 nudge 段后):
    # === ADD1 LANE-SWEEP-01: lane差集三分类(批帽≤8) ===
    if _on('lanesweep'):
        try:
            _ls = st.setdefault('lanesweep_seen', [])
            _new = [f for f in lane_ls('lanes/qlv/inbox') if f not in _ls][:8]
            for _f in _new:
                if '#noauto' in _f:
                    ev.append({'kind':'lanesweep.noauto','ref':_f,'summary':'[lane扫]#noauto入册:'+_f})
                elif lane_age_h('lanes/qlv/inbox/'+_f) > 24:
                    ev.append({'kind':'lanesweep.escalate','ref':_f,'summary':'[lane扫]>24h升己:'+_f,'high_value':True})
                    debt_add('lanesweep:'+_f, 'lane件>24h未理, 升己入债队列')
                else:
                    ev.append({'kind':'lanesweep.task','ref':_f,'summary':'[lane扫]任务件侦得:'+_f,'high_value':True})
                    debt_add('lanetask:'+_f, 'lane任务件候机答/转派')
            st['lanesweep_seen'] = (_ls + _new)[-500:]
        except Exception as e:
            ev.append({'kind':'lanesweep.err','ref':'lanes/qlv/inbox','summary':str(e)[:120]})
    # === ADD2 DEBT-ENGINE-01: 债/FINDING→自驱(每run取1) ===
    if _on('debtengine'):
        try:
            _dq = st.setdefault('debt_queue', [])
            if _dq:
                _d = _dq.pop(0)
                if _d.get('si0_solvable'):
                    ev.append({'kind':'debtengine.exec','ref':_d['id'],'summary':'[债自驱]SI0执行:'+_d['id'],'high_value':True})
                else:
                    ev.append({'kind':'debtengine.seat','ref':_d['id'],'summary':'[债自驱]SI1专属:'+_d['id']+'→覆写位+NUDGE升己','high_value':True})
                    seat_placeholder(_d['id'], _d.get('note',''))
                if 'FINDING' in _d['id'].upper():
                    lane_post('lanes/cisvr/inbox', 'FINDING-QLV-AUTO-'+_d['id'], _d.get('note',''))
            st['debt_queue'] = _dq
            st['debt_backlog'] = len(_dq)
        except Exception as e:
            ev.append({'kind':'debtengine.err','ref':'debt_queue','summary':str(e)[:120]})
(辅助函数 lane_ls/lane_age_h/debt_add/seat_placeholder/lane_post: 照py现 lane_has/probes 族同式, 装时全码附 PATCH.py)
## 件二: .github/workflows/watchtower.yml 补丁
- env 段增: TOWER_PAT: ${{ secrets.TOWER_PAT }} (巡面备用道; GITHUB_TOKEN自写主道不变)
- timeout-minutes: 18 不动(主件四修法已压巡收至秒级)
## 验收(装后L1)
①runs success ②pulse.jsonl seg含lanesweep/debtengine轮转 ③lanesweep_seen/debt_queue落state ④首债自驱件落receipts
——qlv工部 20260915T0330Z #noauto