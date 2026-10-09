/-
CLASSIFY: L1
CERT-CIRC-LEAN-01 · 环状 Sinkhorn 不动点的 leancert Krawczyk 移植（联邦内核锚 CERT-CIRC-01 的 Lean 化身）

系统：k=6 环状成本 C[i][j]=c[(j-i)%%6]，c=[1/2,1/3,2/3,1/4,3/4,1/5]，ε=1，均匀边际；
gauge：f₀ pinned（var 不出现，以 const 0 代入）。变量序：f₁..f₅=var 0..4，g₀..g₅=var 5..10。
方程：Ffᵢ = fᵢ + log 6 + log Σⱼ exp(gⱼ - C[i][j])；Fgⱼ = gⱼ + log 6 + log Σᵢ exp(fᵢ - C[i][j])。
闭形式真解 f*=0, g*=-(log 6 + lse(-c))=-3.154369860822252…；中心有理化 ĝ=-7657889656187/5620014131279；
box 半径 1/10⁹；Python 区间复验：K 宽度 2.04e-14 严格内包，负面控制（中心偏移 1e-6）被拒。
依赖：leancert（github.com/alerad/leancert，Apache-2.0，Zenodo DOI 10.5281/zenodo.21681348）。
-/
import LeanCert.Validity.Krawczyk

namespace FedKernel.CertCirc

open LeanCert.Core LeanCert.Engine LeanCert.Validity

/-- 环状 Sinkhorn gauged 不动点系统（11 维） -/
def circSystem : Fin 11 → Expr :=
  ![(Expr.add (Expr.add (Expr.var 0) (Expr.log (Expr.const 6))) (Expr.log (Expr.add (Expr.add (Expr.add (Expr.add (Expr.add (Expr.exp (Expr.add (Expr.var 5) (Expr.neg (Expr.const (1/5))))) (Expr.exp (Expr.add (Expr.var 6) (Expr.neg (Expr.const (1/2)))))) (Expr.exp (Expr.add (Expr.var 7) (Expr.neg (Expr.const (1/3)))))) (Expr.exp (Expr.add (Expr.var 8) (Expr.neg (Expr.const (2/3)))))) (Expr.exp (Expr.add (Expr.var 9) (Expr.neg (Expr.const (1/4)))))) (Expr.exp (Expr.add (Expr.var 10) (Expr.neg (Expr.const (3/4)))))))),
    (Expr.add (Expr.add (Expr.var 1) (Expr.log (Expr.const 6))) (Expr.log (Expr.add (Expr.add (Expr.add (Expr.add (Expr.add (Expr.exp (Expr.add (Expr.var 5) (Expr.neg (Expr.const (3/4))))) (Expr.exp (Expr.add (Expr.var 6) (Expr.neg (Expr.const (1/5)))))) (Expr.exp (Expr.add (Expr.var 7) (Expr.neg (Expr.const (1/2)))))) (Expr.exp (Expr.add (Expr.var 8) (Expr.neg (Expr.const (1/3)))))) (Expr.exp (Expr.add (Expr.var 9) (Expr.neg (Expr.const (2/3)))))) (Expr.exp (Expr.add (Expr.var 10) (Expr.neg (Expr.const (1/4)))))))),
    (Expr.add (Expr.add (Expr.var 2) (Expr.log (Expr.const 6))) (Expr.log (Expr.add (Expr.add (Expr.add (Expr.add (Expr.add (Expr.exp (Expr.add (Expr.var 5) (Expr.neg (Expr.const (1/4))))) (Expr.exp (Expr.add (Expr.var 6) (Expr.neg (Expr.const (3/4)))))) (Expr.exp (Expr.add (Expr.var 7) (Expr.neg (Expr.const (1/5)))))) (Expr.exp (Expr.add (Expr.var 8) (Expr.neg (Expr.const (1/2)))))) (Expr.exp (Expr.add (Expr.var 9) (Expr.neg (Expr.const (1/3)))))) (Expr.exp (Expr.add (Expr.var 10) (Expr.neg (Expr.const (2/3)))))))),
    (Expr.add (Expr.add (Expr.var 3) (Expr.log (Expr.const 6))) (Expr.log (Expr.add (Expr.add (Expr.add (Expr.add (Expr.add (Expr.exp (Expr.add (Expr.var 5) (Expr.neg (Expr.const (2/3))))) (Expr.exp (Expr.add (Expr.var 6) (Expr.neg (Expr.const (1/4)))))) (Expr.exp (Expr.add (Expr.var 7) (Expr.neg (Expr.const (3/4)))))) (Expr.exp (Expr.add (Expr.var 8) (Expr.neg (Expr.const (1/5)))))) (Expr.exp (Expr.add (Expr.var 9) (Expr.neg (Expr.const (1/2)))))) (Expr.exp (Expr.add (Expr.var 10) (Expr.neg (Expr.const (1/3)))))))),
    (Expr.add (Expr.add (Expr.var 4) (Expr.log (Expr.const 6))) (Expr.log (Expr.add (Expr.add (Expr.add (Expr.add (Expr.add (Expr.exp (Expr.add (Expr.var 5) (Expr.neg (Expr.const (1/3))))) (Expr.exp (Expr.add (Expr.var 6) (Expr.neg (Expr.const (2/3)))))) (Expr.exp (Expr.add (Expr.var 7) (Expr.neg (Expr.const (1/4)))))) (Expr.exp (Expr.add (Expr.var 8) (Expr.neg (Expr.const (3/4)))))) (Expr.exp (Expr.add (Expr.var 9) (Expr.neg (Expr.const (1/5)))))) (Expr.exp (Expr.add (Expr.var 10) (Expr.neg (Expr.const (1/2)))))))),
    (Expr.add (Expr.add (Expr.var 5) (Expr.log (Expr.const 6))) (Expr.log (Expr.add (Expr.add (Expr.add (Expr.add (Expr.add (Expr.exp (Expr.add (Expr.const 0) (Expr.neg (Expr.const (1/2))))) (Expr.exp (Expr.add (Expr.var 0) (Expr.neg (Expr.const (1/5)))))) (Expr.exp (Expr.add (Expr.var 1) (Expr.neg (Expr.const (3/4)))))) (Expr.exp (Expr.add (Expr.var 2) (Expr.neg (Expr.const (1/4)))))) (Expr.exp (Expr.add (Expr.var 3) (Expr.neg (Expr.const (2/3)))))) (Expr.exp (Expr.add (Expr.var 4) (Expr.neg (Expr.const (1/3)))))))),
    (Expr.add (Expr.add (Expr.var 6) (Expr.log (Expr.const 6))) (Expr.log (Expr.add (Expr.add (Expr.add (Expr.add (Expr.add (Expr.exp (Expr.add (Expr.const 0) (Expr.neg (Expr.const (1/3))))) (Expr.exp (Expr.add (Expr.var 0) (Expr.neg (Expr.const (1/2)))))) (Expr.exp (Expr.add (Expr.var 1) (Expr.neg (Expr.const (1/5)))))) (Expr.exp (Expr.add (Expr.var 2) (Expr.neg (Expr.const (3/4)))))) (Expr.exp (Expr.add (Expr.var 3) (Expr.neg (Expr.const (1/4)))))) (Expr.exp (Expr.add (Expr.var 4) (Expr.neg (Expr.const (2/3)))))))),
    (Expr.add (Expr.add (Expr.var 7) (Expr.log (Expr.const 6))) (Expr.log (Expr.add (Expr.add (Expr.add (Expr.add (Expr.add (Expr.exp (Expr.add (Expr.const 0) (Expr.neg (Expr.const (2/3))))) (Expr.exp (Expr.add (Expr.var 0) (Expr.neg (Expr.const (1/3)))))) (Expr.exp (Expr.add (Expr.var 1) (Expr.neg (Expr.const (1/2)))))) (Expr.exp (Expr.add (Expr.var 2) (Expr.neg (Expr.const (1/5)))))) (Expr.exp (Expr.add (Expr.var 3) (Expr.neg (Expr.const (3/4)))))) (Expr.exp (Expr.add (Expr.var 4) (Expr.neg (Expr.const (1/4)))))))),
    (Expr.add (Expr.add (Expr.var 8) (Expr.log (Expr.const 6))) (Expr.log (Expr.add (Expr.add (Expr.add (Expr.add (Expr.add (Expr.exp (Expr.add (Expr.const 0) (Expr.neg (Expr.const (1/4))))) (Expr.exp (Expr.add (Expr.var 0) (Expr.neg (Expr.const (2/3)))))) (Expr.exp (Expr.add (Expr.var 1) (Expr.neg (Expr.const (1/3)))))) (Expr.exp (Expr.add (Expr.var 2) (Expr.neg (Expr.const (1/2)))))) (Expr.exp (Expr.add (Expr.var 3) (Expr.neg (Expr.const (1/5)))))) (Expr.exp (Expr.add (Expr.var 4) (Expr.neg (Expr.const (3/4)))))))),
    (Expr.add (Expr.add (Expr.var 9) (Expr.log (Expr.const 6))) (Expr.log (Expr.add (Expr.add (Expr.add (Expr.add (Expr.add (Expr.exp (Expr.add (Expr.const 0) (Expr.neg (Expr.const (3/4))))) (Expr.exp (Expr.add (Expr.var 0) (Expr.neg (Expr.const (1/4)))))) (Expr.exp (Expr.add (Expr.var 1) (Expr.neg (Expr.const (2/3)))))) (Expr.exp (Expr.add (Expr.var 2) (Expr.neg (Expr.const (1/3)))))) (Expr.exp (Expr.add (Expr.var 3) (Expr.neg (Expr.const (1/2)))))) (Expr.exp (Expr.add (Expr.var 4) (Expr.neg (Expr.const (1/5)))))))),
    (Expr.add (Expr.add (Expr.var 10) (Expr.log (Expr.const 6))) (Expr.log (Expr.add (Expr.add (Expr.add (Expr.add (Expr.add (Expr.exp (Expr.add (Expr.const 0) (Expr.neg (Expr.const (1/5))))) (Expr.exp (Expr.add (Expr.var 0) (Expr.neg (Expr.const (3/4)))))) (Expr.exp (Expr.add (Expr.var 1) (Expr.neg (Expr.const (1/4)))))) (Expr.exp (Expr.add (Expr.var 2) (Expr.neg (Expr.const (2/3)))))) (Expr.exp (Expr.add (Expr.var 3) (Expr.neg (Expr.const (1/3)))))) (Expr.exp (Expr.add (Expr.var 4) (Expr.neg (Expr.const (1/2))))))))]

/-- 候选盒：中心 (0×5, ĝ×6)，半径 1/10⁹ -/
def circBox : Fin 11 → IntervalRat :=
  ![⟨(-(1/1000000000 : ℚ)), (1/1000000000 : ℚ), by norm_num⟩,
    ⟨(-(1/1000000000 : ℚ)), (1/1000000000 : ℚ), by norm_num⟩,
    ⟨(-(1/1000000000 : ℚ)), (1/1000000000 : ℚ), by norm_num⟩,
    ⟨(-(1/1000000000 : ℚ)), (1/1000000000 : ℚ), by norm_num⟩,
    ⟨(-(1/1000000000 : ℚ)), (1/1000000000 : ℚ), by norm_num⟩,
    ⟨((-7657889656187/5620014131279 : ℚ) - (1/1000000000 : ℚ)), ((-7657889656187/5620014131279 : ℚ) + (1/1000000000 : ℚ)), by norm_num⟩,
    ⟨((-7657889656187/5620014131279 : ℚ) - (1/1000000000 : ℚ)), ((-7657889656187/5620014131279 : ℚ) + (1/1000000000 : ℚ)), by norm_num⟩,
    ⟨((-7657889656187/5620014131279 : ℚ) - (1/1000000000 : ℚ)), ((-7657889656187/5620014131279 : ℚ) + (1/1000000000 : ℚ)), by norm_num⟩,
    ⟨((-7657889656187/5620014131279 : ℚ) - (1/1000000000 : ℚ)), ((-7657889656187/5620014131279 : ℚ) + (1/1000000000 : ℚ)), by norm_num⟩,
    ⟨((-7657889656187/5620014131279 : ℚ) - (1/1000000000 : ℚ)), ((-7657889656187/5620014131279 : ℚ) + (1/1000000000 : ℚ)), by norm_num⟩,
    ⟨((-7657889656187/5620014131279 : ℚ) - (1/1000000000 : ℚ)), ((-7657889656187/5620014131279 : ℚ) + (1/1000000000 : ℚ)), by norm_num⟩]

/-- Krawczyk 证书：有理中心 + 解析 Jacobian 逆的有理化预条件子 -/
def circCert : KrawczykCert 11 where
  center := ![0, 0, 0, 0, 0, (-7657889656187/5620014131279 : ℚ), (-7657889656187/5620014131279 : ℚ), (-7657889656187/5620014131279 : ℚ), (-7657889656187/5620014131279 : ℚ), (-7657889656187/5620014131279 : ℚ), (-7657889656187/5620014131279 : ℚ)]
  preconditioner := !![
  [(3574409357/1764367935), (8881752361/8868865447), (2042787816/1995196177), (5427137058/5416123439), (9840068250/9605374853), (-4235486125/3960518378), (-329522625/335335427), (-10595236665/9929132063), (-7915984401/8396097142), (-621369267/568182548), (-4675689813/5070942730)];
  [(8881752361/8868865447), (17384080373/8679428534), (9852574954/9843984949), (2374971757/2371525809), (5427137058/5416123439), (-8871770680/9174065301), (-35246657/34297996), (-9939872018/9694428065), (-2716198885/2756248589), (-7664340829/7573518372), (-6378071246/6434499917)];
  [(2408079782/2351977791), (9852574954/9843984949), (11114975717/5489620430), (9852574954/9843984949), (2042787816/1995196177), (-5387718433/5089359716), (-6895690299/7276381700), (-5332125003/4879717745), (-9304998953/9631490005), (-4554196153/4228419652), (-2311429529/2480037456)];
  [(4899979433/4890035607), (8881752361/8868865447), (6045648877/6040377955), (17384080373/8679428534), (7985148398/7973562405), (-4040651144/4133286111), (-1142611141/1123029312), (-748087916/754947373), (-3489429108/3449157409), (-5181066435/5001719279), (-8649854390/8869401061)];
  [(9840068250/9605374853), (5427137058/5416123439), (2042787816/1995196177), (2374971757/2371525809), (20245947138/9993623107), (-1987682089/1905331944), (-9286442987/9685477735), (-10592435963/9780015482), (-4281172748/4592162759), (-3470066251/3143656436), (-6174783571/6455876376)];
  [(-4235486125/3960518378), (-5553847489/5743087978), (-10535110635/9951701882), (-6717769843/6871779770), (-1987682089/1905331944), (15807763845/8444454854), (4460159150/5381798393), (2317478286/2591151371), (6815633639/8379749925), (8993338798/9938261483), (5147676789/6414210701)];
  [(-7683136008/7818667061), (-8409962054/8183608587), (-6814286385/7190483708), (-1142611141/1123029312), (-9286442987/9685477735), (4460159150/5381798393), (15403023012/8503311991), (596464945/699572216), (7847704467/9884033516), (4254543444/4925760457), (7825653297/9984818689)];
  [(-10595236665/9929132063), (-9939872018/9694428065), (-8818706617/8070478307), (-748087916/754947373), (-3329822766/3074431445), (5815117701/6501830155), (596464945/699572216), (17995968689/9374366510), (211795069/253152531), (4853958203/5226133547), (3035451981/3670491211)];
  [(-7915984401/8396097142), (-3465418749/3516515521), (-6254102747/6473544855), (-9062736039/8958142489), (-453317396/486246967), (2731401877/3358229900), (6124009216/7713072351), (211795069/253152531), (8138712253/4573730122), (124272814/146691825), (2124926497/2767654431)];
  [(-9088652389/8310700169), (-8682873199/8579981131), (-3380699669/3138867198), (-5181066435/5001719279), (-2010898026/1821744043), (305010362/337057549), (3099145614/3588081569), (4853958203/5226133547), (124272814/146691825), (19406247436/9999211223), (6922120338/8270683723)];
  [(-4675689813/5070942730), (-6378071246/6434499917), (-4464588264/4790259007), (-7585977952/7778521795), (-6174783571/6455876376), (2293177366/2857390509), (499116399/636826928), (617796099/747043658), (3754089905/4889591981), (5634451487/6732151989), (16306185199/9270135049)]]

/-- 机检：Krawczyk 全部条件成立（AD 支持 ∧ 中心在盒内 ∧ 预条件子非奇异 ∧ 收缩 <1 ∧ 牛顿像严格内包） -/
example : krawczykCheck circSystem circBox circCert = true := by native_decide

/-- 主定理：盒内存在唯一实根（gauged 不动点唯一性，机器认证） -/
theorem circ_unique_root : ∃! p, FinBoxMem p circBox ∧ SystemZero circSystem p := by
  apply verify_unique_system_root circSystem circBox circCert {}
  native_decide

end FedKernel.CertCirc
