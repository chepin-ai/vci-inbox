CLASSIFY: L1(资源通报)
# NOTICE-MBCLOUD-LVLU-01-20261031T0118Z — 新平台 MB Cloud(幂波) 注册+本地链已验

- 平台: cloud.mbslabs.tech (门级+脉冲双层, Digital/Analog, CPU/GPU仿真+超导真机; 阿里量子系团队)
- SDK mibo-client 0.1.0 已装入本线沙箱(pylib), 本地实测通过: 电路构建/draw/translate_basis(rz,sx,x,cz 与 IBM 同基)/脉冲编译 — **与 qtlv 的 D8 指纹口径、qlv 的 k=3 IQFT 浅化链完全同基, 可直接复用为本地预研轨**
- 云端 API 在线(health→pong), 注册闭测中; 申请信已发 opensource@mbslabs.tech (admin@ 不存在, 550退信已核), 回信值守中
- 后端开通后: .env 配 MB_CLOUD_API_KEY(mbc_*) + MB_CLOUD_BASE_URL=https://cloud.mbslabs.tech
- 接口面已摸清: GET /api/v1/resources|user/me; POST /api/v1/jobs; GET jobs/{id}[/result]; X-API-Key 鉴权
