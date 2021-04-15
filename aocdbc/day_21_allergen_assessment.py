from typing import List, Dict, Set, TYPE_CHECKING
from icontract import require, ensure, DBC
import regex as re  # type: ignore


class Ingredient(str):
    @require(lambda identifier: re.match("^[a-zA-Z]+$", identifier))
    def __init__(self, identifier: str) -> None:
        super().__init__()
        self.identifier: str = identifier


class Allergen(DBC):
    @require(lambda identifier: re.match("^[a-zA-Z]+$", identifier))
    def __init__(self, identifier: str) -> None:
        self.identifier: str = identifier
        self.potential_ingredients: List[Set[Ingredient]] = []

    def __repr__(self) -> str:
        return "{}, {}".format(self.identifier, self.potential_ingredients)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Allergen):
            return NotImplemented
        return (
            self.identifier == other.identifier
            and self.potential_ingredients == other.potential_ingredients
        )

    def add_potential_ingredients_set(
        self, potential_ingredients: Set[Ingredient]
    ) -> None:
        self.potential_ingredients.append(set(potential_ingredients))

    def intersection_potential_ingredients(self) -> Set[Ingredient]:
        return set.intersection(*self.potential_ingredients)


# small error: this allows for "ing1 ing2 (contains , soy, water)"
ALLERGEN_LINE_RE = re.compile(
    r"^(?:\s?(?P<ingredient>\w+))* " r"\(contains (?:(?:,\s)?(?P<allergen>\w+))*\)$"
)


@require(lambda line_1: ALLERGEN_LINE_RE.match(line_1))
@require(lambda line_2: ALLERGEN_LINE_RE.match(line_2))
def is_equal_ingredient_line(line_1: str, line_2: str) -> bool:
    ingredients_in_line_1 = set(ALLERGEN_LINE_RE.match(line_1).captures(1))
    allergens_in_line_1 = set(ALLERGEN_LINE_RE.match(line_1).captures(2))

    ingredients_in_line_2 = set(ALLERGEN_LINE_RE.match(line_2).captures(1))
    allergens_in_line_2 = set(ALLERGEN_LINE_RE.match(line_2).captures(2))

    return (
        ingredients_in_line_1 == ingredients_in_line_2
        and allergens_in_line_1 == allergens_in_line_2
    )


@require(
    lambda ingredient_list_1: all(
        ALLERGEN_LINE_RE.match(line) for line in ingredient_list_1
    )
)
@require(
    lambda ingredient_list_2: all(
        ALLERGEN_LINE_RE.match(line) for line in ingredient_list_2
    )
)
def is_equal_ingredient_list(
    ingredient_list_1: List[str], ingredient_list_2: List[str]
) -> bool:
    if len(ingredient_list_1) != len(ingredient_list_2):
        return False
    for l1 in ingredient_list_1:
        if not any(is_equal_ingredient_line(l1, l2) for l2 in ingredient_list_2):
            return False
    for l2 in ingredient_list_2:
        if not any(is_equal_ingredient_line(l2, l1) for l1 in ingredient_list_1):
            return False
    return True


@require(lambda lines: all(ALLERGEN_LINE_RE.match(line) for line in lines))
@ensure(lambda result, lines: is_equal_ingredient_list(serialize(result), lines))  # type: ignore
def parse_list_of_foods(lines: List[str]) -> List[Allergen]:
    allergens: Dict[str, Allergen] = dict()
    for line in lines:
        ingredients_in_line = ALLERGEN_LINE_RE.match(line).captures(1)
        allergens_in_line = ALLERGEN_LINE_RE.match(line).captures(2)
        for allergen in allergens_in_line:
            if allergen not in allergens:
                allergens[allergen] = Allergen(allergen)
            allergens[allergen].add_potential_ingredients_set(ingredients_in_line)
    return list(allergens.values())


@require(
    lambda allergen_set: all(
        len(allergen.potential_ingredients) > 0 for allergen in allergen_set
    )
)
@ensure(lambda result, allergen_set: allergen_set == parse_list_of_foods(result))
def serialize(allergen_set: List[Allergen]) -> List[str]:
    ingredient_groups: Dict[str, List[Allergen]] = dict()
    for allergen in allergen_set:
        for ingredient_set in allergen.potential_ingredients:
            ingredient_set_str = " ".join(
                [str(ingredient) for ingredient in ingredient_set]
            )
            if str(ingredient_set_str) in ingredient_groups.keys():
                ingredient_groups[str(ingredient_set_str)].append(allergen)
            else:
                ingredient_groups[str(ingredient_set_str)] = [allergen]
    ingredient_list: List[str] = []
    for ingredients, allergens in ingredient_groups.items():
        allergens_str: str = ", ".join(
            [str(allergen.identifier) for allergen in allergens]
        )
        ingredient_list.append("{} (contains {})".format(ingredients, allergens_str))
    return ingredient_list


ALLERGEN_LIST_RE = re.compile(
    r"^(\s?\w+)* \(contains ((,\s)?\w+)*\)" r"(\n(\s?\w+)* \(contains ((,\s)?\w+)*\))*$"
)


@require(lambda puzzle_input: ALLERGEN_LIST_RE.match(puzzle_input))
def solve(puzzle_input: str) -> Set[Ingredient]:
    ingredient_lines = puzzle_input.split("\n")
    allergen_set = parse_list_of_foods(ingredient_lines)
    excluded_ingredients = set.union(
        *map(
            lambda allergen: allergen.intersection_potential_ingredients(), allergen_set
        )
    )
    all_ingredients = set.union(
        *map(lambda allergen: set.union(*allergen.potential_ingredients), allergen_set)
    )
    return all_ingredients.difference(excluded_ingredients)


if __name__ == "__main__":
    ingredient_list_str = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""

    # print(solve(parse_allergen_list(ingredient_list)))
    # print(solve(parse_allergen_list(large_input)))
    # print(parse_list_of_foods(ingredient_list_str.split('\n')))
    # for a in parse_list_of_foods(ingredient_list_str.split('\n')):
    #     print("{}: {}".format(a.identifier, a.intersection_potential_ingredients()))
    # parsed = parse_list_of_foods(ingredient_list_str.split('\n'))
    # print("{}\n\t{}".format('parsed', parsed))
    # serialized = serialize(parsed)
    # print("{}\n\t{}".format('serialized', serialized))
    # print("{}\n\t{}".format('parsed serialized', parse_list_of_foods(serialized)))
    # print("solution")
    # for a in parse_list_of_foods(ingredient_list_str.split('\n')):
    #     print("\t{}: {}".format(a.identifier, a.intersection_potential_ingredients()))
    print(solve(ingredient_list_str))


large_input = """fgrlmbk dmhfc gbc bqjdc nfxjhz htxsjf lkhlq frrns fzpl ckkhgh gtfg cfzdnz qdgsb vcm rfct dvvtfbhc jjhh lbdknnb lrsqdnj gzzpg rqf nlvklmk xfdpmx rpsvg bbbl bpfkb bsfrk zstls srkf dtjkqfd zcvc cll nstk cmbcm xgljlz hpbfvxmj qqmtv lmds hnrdth vbjlmq kdpgj pcbms nrjzp thfjc nrbqn cbmjz lprxj gxkkcxk hsjxkq gskbc tghhr rvgdt dvnbh ppmtvvb xtbjmj mbljqv slkp dvdh nrrvpz (contains shellfish, dairy, nuts)
zstls frrns zcvc slkp knrtx ngbnh rqjdfxm znzb cbmjz jsfp zsf qrxfdsb htxsjf nrrvpz kbjbzdv rqf mkvk tghhr nrbqn bbbl dvgrzqb rvgdt thfjc gzmbgc cfzdnz ttbrlvd dxlzph lbdknnb gbc pscb bskvb jjhh ndhcp sqbn vcm zhmb gzzpg pcbtcc mdpmn mcs dtjkqfd dvnbh xtghfk xzjz cmbcm rlfdl xtbjmj lcqvnp bdq (contains eggs, shellfish)
mkvk xtghfk gzmbgc hnrdth bbbl lmds sxrsr rpx cbmjz thfjc pvfb jmzfqd knrtx slkp dlmvvd ncnm dkctbd dvnbh bhjnl jsfp rcv sgxsvmh zsf qtmvn pcbms srkf pgcd jfjpb jxcfst pcgxqf zstls cmbcm bpfkb zbxpb pllbt sjjq hrllc trgzhs cbxr gfgkvpl mrvskt vbjlmq gxkkcxk zvfpvb fvnf htxsjf btq khpmn rqf dvvtfbhc jhbpz rhmnss lxtt mcs nrjzp kdbzffc snbbqj ckkhgh dxlzph qqmtv jfdzjndd cfzdnz lcqvnp bbvk zxjffp (contains peanuts, soy)
pxjs zmvvf ckkhgh gfgkvpl lmds pgcd cmbcm tllk lxtt ngbnh rpsvg hnrdth qrxfdsb qdgsb kdjxbm cfzdnz rlfdl trgzhs nxvt qgklpvc srdlb vfrvvfr srjgg zhmb slvhb lbdknnb mbljqv lkhlq sjc htxsjf nstk ttbrlvd bpfkb scnr gskbc srpql dgzxvk ptsjmn kbjbzdv xfdpmx rpx dvnbh gkh jhbpz nfxjhz cbxr rjcrs zsf cll cmhsj pxmxd bbbl ncnm cldns pcbms pvfb lrsqdnj bbvk mdpmn lcqvnp vbjlmq kbnhq (contains nuts, peanuts, eggs)
zbxpb pvfb nstk srjgg kbjbzdv vcm kbz rpx qhbrf fgrlmbk xvkpct zsf rqjdfxm cjthv pthsvl ttbrlvd rhmnss zmvvf pllbt cbpnbfr nrjzp bhjnl qgklpvc zstls ljkgg knrtx vlhld hsjxkq tllk pkjhrlnz fvnf cmbcm slkp cbmjz scnr kdbzffc rfct qbvhh bbbl bvcnmx htxsjf nrbqn dkctbd cxsv gjfbc snbbqj rpsvg dvdh sjjq sqbn jnlkg jsfp sqrmn qdgsb ckkhgh bskvb gkh slvhb dsdfkts xdbx vnbfkbm rcv thfjc rlfdl dlmvvd cfzdnz mszc pgcd bdq zdxfcln dvnbh znzb qtmvn nlvklmk (contains wheat, nuts)
mkvk cqnq cmbcm rqjdfxm mbljqv rhmnss dsdfkts bknqz htxsjf cll qrxfdsb cbxr mszc slvhb mkflxv zsf hpbfvxmj nmqph cxsv bskvb trgzhs lmds mdpmn npkz cfzdnz hnrdth xbvjrd ml lprxj jjhh zxjffp mcs cbmjz qtmvn nxvt pkjhrlnz pllbt kdpgj gfgkvpl lslkm gtfg kdjxbm jnlkg snbbqj gzzpg dvnbh mklc bbbl zgnvx ncnm gdtfv nlvklmk ckkhgh qbvhh fddk slkp sjc (contains wheat)
nmqph gzzpg txkpq rqf khpmn lxtt xtghfk lcqvnp kbjbzdv npgktnl mstcz jfjpb ncnm mlh dvnbh zvfpvb nthdsp tghhr xfdpmx sgxsvmh mkvk vnbfkbm pgcd rjcrs ttbrlvd tchncfl hpbfvxmj kbz nstk vbjlmq pkjhrlnz rfct cbmjz cldns bbbl pxjs dkctbd nlvklmk cfzdnz ndhcp lrsqdnj pcbtcc tgqcfpk htxsjf hfps xbvjrd lmds qrxfdsb kdbzffc nfxjhz srpql jmzfqd zdxfcln kbnhq pscb (contains fish)
cmhsj gbc gkh ptsjmn vbjlmq bskvb slvhb kbjbzdv vfrvvfr dmhfc srkf nrrvpz snbbqj cbmjz jfdzjndd cmbcm mkflxv bxv sgxsvmh gzmbgc htxsjf zgnvx ncnm qqmtv nlvklmk lxtt mrvskt cbpnbfr hhjvrh jjhh sqrmn vnbfkbm rrdf xtbjmj cfzdnz btltc pxmxd qdgsb gdtfv fhxtgj lkhlq bpfkb sjc ttbrlvd lbdknnb bdq pvfb nrbqn gzzpg pthsvl txkpq lmds mszc kdbzffc zcvc hfps pkjhrlnz dtjkqfd jxcfst khpmn fddk jhbpz bbbl dvdh pcgxqf rqjdfxm srdlb bbvk bknqz lslkm srjgg gjfbc tllk kdjxbm thfjc mklc mstcz dxlzph hpbfvxmj qlmjk sqbn (contains dairy, shellfish, fish)
rvgdt vcm zxjffp ptsjmn zdxfcln lbdknnb qdgsb cfzdnz ttbrlvd qxcrc gkh dsdfkts bhjnl lslkm cbxr btq dkctbd hrllc lmds qrxfdsb npgktnl gxkkcxk pllbt jmzfqd pcbms cxsv xcbpv fqpn fhxtgj btltc hsjxkq rlfdl hfps rqf bsfrk fvnf skfqm npkz sjc fzpl bqjdc hpbfvxmj mbljqv lcdfs gfgkvpl cbmjz cj trgzhs rhmnss mklc zgnvx kbz qsddtd htxsjf nfxjhz sjjq nlvklmk gzmbgc zbxpb qqmtv cmbcm bknqz mrvskt ngbnh jfjpb thfjc nrjzp dlmvvd znzb xbvjrd ml fgrlmbk fbccmpv mcs mstcz xtbjmj bbbl qhbrf lrsqdnj xfdpmx gtfg bskvb (contains nuts, dairy, peanuts)
bskvb rjcrs bbvk fkmzx zxjffp gkh gskbc gbc npkz nlvklmk mszc hpbfvxmj npgktnl qtmvn cfzdnz xbvjrd vfrvvfr cmbcm mbljqv hnrdth lprxj kdjxbm sxrsr qgklpvc lslkm bbbl qrxfdsb mkflxv htxsjf gzzpg fddk ljkgg rfct cll gxkkcxk srkf lcqvnp dkctbd pkjhrlnz bhjnl bsfrk xgljlz tgqcfpk kdbzffc cxsv jnlkg sgxsvmh rpsvg tchncfl vnbfkbm khpmn pcbtcc jfdzjndd cbmjz sjjq zstls xhgfc nthdsp btq zvfpvb sqrmn ttbrlvd txkpq nxvt lrsqdnj lmds ngbnh (contains shellfish, soy)
nxvt zbxpb xzjz dtjkqfd slkp xfdpmx trgzhs fhxtgj sxrsr cmhsj kdjxbm scnr xdbx kdbzffc dsdfkts ckkhgh mrvskt pscb nrbqn mszc dlmvvd fbccmpv lmds hnrdth rpx cj pllbt sqbn xbvjrd txkpq pvfb rhmnss sjc bbvk cqnq qtmvn dvgrzqb jnlkg skfqm kbnhq thfjc pxmxd lprxj lcdfs bknqz sqrmn rcv rlfdl zvfpvb dvnbh dvdh ttbrlvd jhbpz pthsvl qrxfdsb bsfrk cbmjz frrns srjgg cbpnbfr cfzdnz mcs qbvhh kbz qgklpvc htxsjf dvvtfbhc rpsvg qxcrc dxlzph ptsjmn hhjvrh gjfbc bbbl jznrg xtbjmj (contains fish)
npkz sjc fgrlmbk ml kdjxbm ttbrlvd rvgdt lmds cjthv cxsv tghhr gxkkcxk bqjdc dsdfkts cj pcgxqf pcbtcc dvnbh gdtfv jjhh htxsjf rlfdl zbxpb pvfb kdpgj bbbl rjcrs fhxtgj lrsqdnj cfzdnz jhbpz xvkpct cbmjz rqjdfxm nthdsp qtmvn vnbfkbm zgnvx pxjs rqf gkh dvvtfbhc npgktnl nrbqn mkflxv pcbms fbccmpv qdgsb pxmxd srkf jznrg bpfkb cbxr zmvvf jfdzjndd xhgfc vfrvvfr fddk mlh xfdpmx (contains shellfish, dairy, peanuts)
vcm mstcz skfqm pxmxd sgxsvmh xtbjmj bhjnl dvdh zbxpb dxlzph gzmbgc dvgrzqb gfgkvpl xcbpv gskbc jhbpz npkz lmds bbbl nfxjhz ml gxkkcxk dvnbh ngbnh zdxfcln kdjxbm mkvk zvfpvb zcvc jjhh xbvjrd slkp dgzxvk ndhcp hpbfvxmj ttbrlvd ppmtvvb cmbcm htxsjf pcbms lrsqdnj cfzdnz rvgdt dlmvvd thfjc bbvk bknqz jfjpb jxcfst lslkm btltc txkpq ljkgg nrrvpz qtmvn nrjzp srdlb jsfp nrbqn zmvvf frrns (contains nuts)
zstls bbbl nthdsp bhjnl lmds jjhh zsf xfdpmx cbxr qrxfdsb trgzhs rjcrs dkctbd mkflxv qdgsb vnbfkbm dtjkqfd pcgxqf fbccmpv vcm hrllc qbvhh pcbms lxtt nrbqn tchncfl cj bsfrk bvcnmx npgktnl xhgfc bxv lkhlq nmqph ngbnh ckkhgh jfjpb gkh pcbtcc nrjzp lrsqdnj mrvskt mlh fkmzx cfzdnz gdtfv tghhr fqpn ljkgg btq gtfg jsfp pxmxd kdpgj dvgrzqb dvnbh qtmvn pthsvl bskvb lbdknnb bqjdc ttbrlvd hfps mbljqv gzzpg cmbcm mklc pxjs thfjc xcbpv cbmjz (contains shellfish, nuts, fish)
jfdzjndd jxcfst dtjkqfd cxsv ttbrlvd bhjnl rqjdfxm rjcrs scnr trgzhs ml pvfb qhbrf cmbcm cbmjz cll tchncfl nlvklmk nrrvpz qqmtv jnlkg mrvskt mkflxv npgktnl bxv srdlb kbnhq jsfp ngbnh dvnbh vfrvvfr dgzxvk lcqvnp gjfbc srpql nfxjhz cfzdnz lkhlq xdbx xvkpct xtghfk bsfrk txkpq rhmnss gdtfv bpfkb rlfdl rqf fddk jznrg rvgdt vnbfkbm jfjpb bbbl kdjxbm xfdpmx htxsjf gzzpg mdpmn mstcz mkvk jjhh knrtx (contains fish, eggs)
qbvhh gtfg gdtfv ckkhgh gzzpg nfxjhz mszc dtjkqfd rfct kbz cbmjz cmbcm jfjpb qdgsb nxvt pxjs fzpl ml rqjdfxm zxjffp pscb pxmxd zdxfcln mkvk cxsv ljkgg lmds srkf jfdzjndd skfqm cll xzjz mrvskt ttbrlvd bqjdc qsddtd txkpq zhmb pvfb xtghfk dvnbh pgcd hsjxkq srjgg vnbfkbm gskbc qlmjk kbjbzdv lcdfs htxsjf zgnvx bbbl vlhld bdq qhbrf mkflxv btltc jnlkg hrllc trgzhs bxv xtbjmj rpx (contains peanuts)
dmhfc bbbl gtfg rlfdl lmds qhbrf qtmvn bdq mkvk fqpn pxmxd pvfb cfzdnz jfjpb qbvhh gbc gzmbgc zbxpb gfgkvpl cmbcm cbpnbfr xtbjmj hrllc pkjhrlnz ml jsfp gskbc srdlb mbljqv qdgsb mlh srkf rfct nfxjhz lcdfs cbmjz rrdf gzzpg dxlzph nrrvpz ttbrlvd kbz sxrsr sgxsvmh pcbms lxtt rhmnss htxsjf scnr fkmzx (contains fish)
chjzv mbljqv jnlkg qdgsb gzmbgc bhjnl gjfbc jjhh trgzhs zdxfcln gbc vbjlmq mcs cmbcm lprxj rhmnss snbbqj khpmn fbccmpv qsddtd xtghfk cqnq qlmjk dkctbd qhbrf kbjbzdv dvnbh hhjvrh cbpnbfr zxjffp rjcrs gzzpg vcm pxjs gtfg rpsvg kbnhq cbmjz fddk hsjxkq jmzfqd cjthv sqrmn bvcnmx lbdknnb gkh bqjdc mkvk rfct lcdfs btltc bdq lmds ttbrlvd scnr htxsjf tchncfl pcgxqf xcbpv zbxpb npgktnl xnffv gxkkcxk slvhb bpfkb dvgrzqb rlfdl tllk sgxsvmh mdpmn tghhr bbbl qgklpvc vlhld znzb kdjxbm fhxtgj qqmtv (contains wheat, fish)
sjc hrllc rlfdl qqmtv srkf fhxtgj chjzv gzmbgc vfrvvfr qtmvn tllk fbccmpv ckkhgh skfqm cmbcm qbvhh jznrg dvvtfbhc qgklpvc ml rvgdt cfzdnz hsjxkq lmds xzjz bpfkb nxvt gzzpg mkflxv pcbtcc ttbrlvd pvfb xnffv fzpl xgljlz sgxsvmh qxcrc pxmxd bdq ngbnh kbnhq pkjhrlnz xtghfk cxsv pthsvl pcbms mlh xvkpct fddk zsf mszc lkhlq cldns rcv htxsjf nfxjhz mcs frrns nrjzp dvgrzqb zdxfcln vnbfkbm znzb dsdfkts rpx srjgg sqbn srpql dtjkqfd cbmjz pgcd pxjs gjfbc zmvvf qhbrf btltc gkh cqnq npkz slkp nrrvpz hfps txkpq rhmnss cbpnbfr rpsvg hpbfvxmj lcdfs zxjffp nrbqn xhgfc mstcz ndhcp zcvc bbbl (contains shellfish, soy, peanuts)
hsjxkq nrbqn lmds hrllc nlvklmk kdbzffc qsddtd lkhlq vnbfkbm rqf npkz bvcnmx btq pxjs srpql zmvvf qdgsb kbjbzdv htxsjf sqbn lxtt zsf rvgdt dlmvvd fqpn hpbfvxmj xtbjmj vbjlmq fkmzx vcm jxcfst xhgfc lcdfs ptsjmn pcgxqf cmbcm ppmtvvb hnrdth xbvjrd jhbpz fddk gbc bbvk bpfkb ttbrlvd bsfrk lslkm thfjc rhmnss bbbl xgljlz jznrg lrsqdnj slkp dvdh pcbtcc dvnbh jmzfqd bhjnl cbpnbfr cfzdnz cxsv tghhr cbxr mstcz (contains wheat, eggs, soy)
qlmjk htxsjf ngbnh fhxtgj zxjffp pscb qgklpvc cqnq mstcz txkpq bsfrk xzjz knrtx npgktnl xdbx lslkm fbccmpv kbz tgqcfpk lcqvnp nrrvpz mkvk xtghfk bskvb ncnm kbnhq gkh qbvhh bbbl vcm sqbn dvnbh ml xgljlz sjjq vlhld jhbpz ttbrlvd vnbfkbm tllk hsjxkq bpfkb cmhsj rhmnss nthdsp gzmbgc fkmzx xtbjmj srjgg jjhh xnffv cbmjz mcs rlfdl dxlzph ppmtvvb hpbfvxmj lxtt cj bknqz qtmvn pxmxd scnr bxv kdpgj gdtfv cfzdnz gxkkcxk cmbcm nstk sqrmn fgrlmbk xcbpv kdbzffc hnrdth xfdpmx lbdknnb bvcnmx qsddtd (contains soy)
thfjc dvnbh ppmtvvb pscb mkflxv lmds rpx ml gbc znzb srkf nxvt mklc cmbcm xbvjrd dvvtfbhc nmqph vfrvvfr xtbjmj qbvhh htxsjf mlh khpmn zxjffp kdbzffc slvhb sjjq kdjxbm mstcz jznrg lcdfs fhxtgj btq kdpgj dsdfkts skfqm qtmvn bxv bbvk kbz sgxsvmh jfdzjndd mszc jsfp cbmjz rqf bdq zmvvf zstls hnrdth tgqcfpk qxcrc zdxfcln ttbrlvd pxjs cfzdnz npkz dgzxvk nrbqn pcbms tchncfl rqjdfxm fvnf cmhsj sqbn cbpnbfr jhbpz qdgsb xcbpv cbxr (contains soy, wheat)
rfct rcv knrtx pxjs lslkm pcbms gxkkcxk txkpq lxtt zgnvx lkhlq cmbcm dtjkqfd cbpnbfr gdtfv rpx bbvk jsfp zsf lprxj jnlkg mkflxv ml fvnf pvfb sxrsr jmzfqd ckkhgh bknqz ttbrlvd lmds hrllc gtfg mdpmn pscb gjfbc slvhb npkz zbxpb xhgfc zxjffp ndhcp jfdzjndd pthsvl vlhld jznrg tchncfl xzjz hhjvrh bhjnl nthdsp jxcfst nmqph nlvklmk rqjdfxm cmhsj fqpn vcm vfrvvfr mrvskt xgljlz dvnbh qhbrf htxsjf cll srkf gbc thfjc lbdknnb pxmxd zmvvf bbbl rhmnss kdpgj vnbfkbm cbmjz zhmb (contains eggs)
nstk dvgrzqb nrrvpz qbvhh nmqph gdtfv gtfg kdbzffc nlvklmk hpbfvxmj cbmjz snbbqj xvkpct mbljqv dtjkqfd gzzpg pvfb fvnf mkvk sqrmn dgzxvk fbccmpv gzmbgc rrdf sjjq txkpq lmds pxmxd zstls ttbrlvd pcgxqf xbvjrd mrvskt htxsjf dvnbh xdbx cfzdnz slkp vnbfkbm tchncfl btltc nthdsp sgxsvmh xfdpmx kdjxbm ncnm ndhcp rlfdl qrxfdsb cmbcm mcs gskbc lslkm trgzhs pkjhrlnz (contains soy)
lmds ptsjmn ljkgg pxjs thfjc hpbfvxmj fkmzx znzb ngbnh fqpn tghhr qdgsb dtjkqfd mklc dkctbd hnrdth pxmxd cfzdnz gdtfv fhxtgj mstcz rpx qlmjk xtghfk htxsjf bqjdc gbc jznrg pcbms tllk jfdzjndd khpmn pcgxqf hsjxkq rqjdfxm qgklpvc zsf hfps sqrmn dvgrzqb pvfb trgzhs bbvk nmqph dsdfkts lbdknnb jnlkg cbmjz zgnvx lslkm vfrvvfr gtfg gjfbc bsfrk ttbrlvd mlh dvnbh jxcfst xtbjmj bbbl rqf gskbc zvfpvb nrjzp kbnhq pgcd ncnm qbvhh mbljqv mrvskt (contains shellfish, eggs)
lbdknnb jhbpz knrtx sqbn fhxtgj dmhfc bpfkb pxmxd zhmb dvgrzqb fbccmpv qdgsb mlh slkp qhbrf jnlkg bknqz dvnbh ttbrlvd lslkm qrxfdsb ml cxsv xdbx btq cbmjz cqnq zdxfcln xhgfc qtmvn dkctbd fddk cfzdnz lmds rfct xtbjmj rqf slvhb bxv cmbcm gdtfv kdpgj ckkhgh rlfdl cj dtjkqfd jsfp srpql bbbl nrrvpz fvnf (contains fish)
zbxpb fddk scnr gxkkcxk nrrvpz xfdpmx bsfrk hfps cbmjz dxlzph nthdsp dmhfc vnbfkbm tghhr lmds slkp cmbcm cmhsj nlvklmk cfzdnz sqbn hnrdth pkjhrlnz btltc pcbms kbz cbxr rqjdfxm cxsv mkvk zvfpvb zmvvf kdpgj bbbl dlmvvd mlh mbljqv pscb rlfdl bqjdc qqmtv ckkhgh qbvhh pxjs sqrmn pthsvl fbccmpv pvfb qrxfdsb znzb mrvskt rrdf bbvk jfdzjndd vcm ttbrlvd nfxjhz jfjpb fkmzx skfqm cbpnbfr dvnbh gdtfv lcdfs nrjzp xbvjrd (contains peanuts)
bhjnl gbc pthsvl vlhld mklc cbmjz sxrsr mkflxv cjthv rrdf pgcd bbbl dxlzph sjjq rjcrs mszc snbbqj lmds btq fzpl srjgg lprxj gskbc npgktnl cbxr lslkm kdjxbm jmzfqd pscb hfps xzjz khpmn sgxsvmh srkf vnbfkbm jnlkg xnffv xhgfc bvcnmx rqf zcvc jfdzjndd bbvk lcqvnp bknqz gzzpg ttbrlvd fbccmpv hrllc qgklpvc cmbcm cfzdnz frrns dvnbh kbz qsddtd qxcrc nmqph sjc xvkpct jsfp bskvb xbvjrd hsjxkq jhbpz gtfg (contains fish)
znzb fbccmpv pthsvl pxmxd ttbrlvd btltc fzpl knrtx bhjnl nmqph dvnbh btq cfzdnz nstk nlvklmk pcgxqf dlmvvd zsf bpfkb cmbcm snbbqj bxv xtbjmj frrns sxrsr qrxfdsb bskvb htxsjf ppmtvvb qdgsb cbmjz slkp xfdpmx srjgg qbvhh qqmtv zvfpvb zstls jnlkg xbvjrd cbxr zcvc tchncfl zhmb gtfg bdq gzzpg bbbl chjzv scnr kbz (contains wheat, soy)
dxlzph ljkgg tchncfl ncnm srjgg bbbl lmds kbjbzdv znzb cll dmhfc vbjlmq ttbrlvd rcv zsf nrbqn kdpgj zcvc btq cjthv mcs vfrvvfr cfzdnz jhbpz gzzpg cmbcm gxkkcxk jjhh fbccmpv jnlkg qsddtd cbmjz zvfpvb npgktnl htxsjf mdpmn thfjc nmqph xdbx fqpn lprxj mrvskt qgklpvc gtfg lcdfs pkjhrlnz zdxfcln slkp xhgfc mlh zstls bdq gfgkvpl jfdzjndd ckkhgh ngbnh (contains peanuts)
bknqz fgrlmbk tchncfl qtmvn tllk cmbcm sjjq gkh cbmjz ttbrlvd pvfb kdjxbm lslkm thfjc dvvtfbhc vbjlmq knrtx cxsv dmhfc bskvb dlmvvd sjc zsf snbbqj mbljqv bbbl qhbrf pkjhrlnz mrvskt khpmn ckkhgh pthsvl dxlzph zstls gxkkcxk nstk sgxsvmh fvnf lmds fqpn zhmb tghhr rfct gskbc nthdsp xdbx cmhsj ptsjmn gfgkvpl rlfdl mklc rqf cll tgqcfpk srjgg dvnbh pcbtcc cjthv dkctbd jjhh sqbn vlhld sxrsr ndhcp htxsjf pgcd hnrdth fddk qqmtv xbvjrd (contains soy, nuts)
kbnhq dgzxvk kbz lbdknnb lrsqdnj cbmjz jhbpz vcm tghhr nrbqn bbvk mdpmn btltc xzjz htxsjf jfjpb cldns lcdfs fbccmpv xvkpct vfrvvfr ptsjmn mklc trgzhs rrdf lmds khpmn xdbx rpx sxrsr bskvb mkflxv sjc lkhlq gdtfv cbpnbfr jjhh nmqph cqnq srjgg bbbl pxjs zxjffp ttbrlvd cmbcm nxvt zcvc zmvvf vlhld npkz bpfkb hpbfvxmj pxmxd bvcnmx nthdsp cfzdnz pvfb nstk mbljqv rfct nlvklmk bhjnl srpql pcbms cmhsj bqjdc pllbt rqjdfxm qhbrf dmhfc dvdh sqbn btq bxv pscb qbvhh qrxfdsb xfdpmx (contains fish, shellfish)
bbbl trgzhs cmbcm nfxjhz dgzxvk jznrg xtbjmj ljkgg zgnvx dvnbh sxrsr pxjs jhbpz hrllc cfzdnz rpx kbz dsdfkts btltc sjc pllbt vcm xnffv vbjlmq pxmxd xgljlz hhjvrh sjjq qbvhh bdq fhxtgj pscb qqmtv xfdpmx gzzpg zmvvf mszc mrvskt cbmjz ngbnh zhmb jfjpb qdgsb dvvtfbhc mkflxv slvhb kdpgj lmds pgcd qrxfdsb ptsjmn fqpn nxvt nmqph zcvc mkvk zsf zbxpb vnbfkbm dtjkqfd dvdh pcbtcc fkmzx lcdfs zxjffp cbpnbfr tllk ttbrlvd knrtx dxlzph pvfb (contains wheat, shellfish, dairy)
rpsvg tchncfl pscb ljkgg ptsjmn fddk kbjbzdv pcbms mkvk cbmjz lbdknnb jjhh pvfb bqjdc sqbn khpmn npgktnl nfxjhz srpql qbvhh xcbpv gfgkvpl cmbcm lcqvnp znzb zmvvf tgqcfpk xfdpmx bhjnl ndhcp cj cbpnbfr kdpgj scnr cldns zhmb trgzhs zsf nstk xtbjmj xzjz dvnbh lxtt bvcnmx qdgsb qgklpvc dsdfkts lmds ngbnh rqjdfxm jfjpb lrsqdnj gtfg cjthv mklc zbxpb zgnvx gzzpg vnbfkbm bbbl htxsjf txkpq cfzdnz rlfdl dlmvvd srjgg slvhb rjcrs (contains shellfish, wheat)
tchncfl qlmjk npkz vlhld hhjvrh dkctbd sxrsr btq lxtt lrsqdnj lcqvnp qxcrc lslkm cbmjz nmqph xbvjrd cbxr rpsvg knrtx bbbl gxkkcxk mlh kbz btltc lmds rvgdt gjfbc bxv xdbx txkpq zbxpb hpbfvxmj zdxfcln snbbqj cxsv cmbcm cjthv hfps rpx pcbtcc gfgkvpl rrdf jfjpb tllk dvnbh mkflxv sjc nrbqn zhmb ttbrlvd pxjs srdlb ncnm pkjhrlnz ppmtvvb xvkpct hrllc nthdsp gzzpg kdbzffc hnrdth xcbpv mrvskt dvdh bvcnmx lcdfs ngbnh cfzdnz nrrvpz kdjxbm jsfp rqjdfxm zsf tghhr frrns fqpn xgljlz ndhcp jjhh xhgfc (contains dairy, soy, shellfish)
frrns lslkm rqjdfxm slvhb htxsjf cbxr dtjkqfd tgqcfpk hsjxkq nstk cmbcm cqnq ljkgg lkhlq jfdzjndd nlvklmk ttbrlvd gjfbc pthsvl thfjc cmhsj dgzxvk pxmxd pkjhrlnz zstls znzb sjc btltc xvkpct knrtx mlh bbbl zvfpvb lmds khpmn gdtfv cldns bdq dvvtfbhc cbmjz vcm mstcz qqmtv slkp dvnbh ngbnh mbljqv gkh kbjbzdv hfps (contains shellfish)
chjzv rrdf hpbfvxmj qsddtd cldns vbjlmq sqrmn bbbl htxsjf cqnq pcgxqf fbccmpv dtjkqfd xhgfc bqjdc fzpl qhbrf nstk nlvklmk bpfkb zmvvf trgzhs dvdh dlmvvd tgqcfpk qbvhh knrtx xtghfk xcbpv pxjs gskbc xgljlz srpql qrxfdsb rjcrs pscb pthsvl bhjnl fkmzx qlmjk zcvc bdq gzzpg bknqz tchncfl vcm cmbcm cbmjz kbjbzdv cjthv srjgg gbc rcv ttbrlvd jhbpz txkpq ppmtvvb btltc pvfb btq dvnbh pllbt lmds lcqvnp mstcz npkz cbxr bvcnmx kdbzffc (contains shellfish, fish)
nthdsp gbc zgnvx sqrmn fddk slvhb rqjdfxm hsjxkq bsfrk kdbzffc dkctbd mbljqv kbz cbpnbfr ngbnh zdxfcln qxcrc srjgg pvfb mlh khpmn gdtfv cbmjz sxrsr ttbrlvd mkvk mrvskt dvdh gskbc thfjc qtmvn pthsvl vfrvvfr pllbt tllk vnbfkbm dvgrzqb xdbx kbnhq cmbcm dmhfc jnlkg bdq ndhcp bpfkb rlfdl htxsjf cqnq cfzdnz xnffv bbbl tgqcfpk gtfg lmds pxjs (contains fish, dairy)
gzmbgc fzpl nlvklmk sjjq mrvskt kdbzffc sqrmn gjfbc qdgsb lxtt sxrsr tchncfl lrsqdnj qrxfdsb zmvvf cll bsfrk pcbtcc zhmb fhxtgj lprxj cjthv fgrlmbk rpsvg hpbfvxmj ttbrlvd qsddtd npkz nrbqn ppmtvvb snbbqj tghhr mlh lbdknnb cfzdnz xvkpct fbccmpv dlmvvd rrdf xtbjmj lcqvnp vlhld rlfdl nfxjhz jhbpz htxsjf dvnbh dvdh jmzfqd rjcrs tgqcfpk ncnm btltc skfqm jjhh xgljlz qxcrc lmds cqnq jznrg bskvb rpx dxlzph lslkm gbc hsjxkq jxcfst rvgdt cbmjz xfdpmx cmbcm srpql rcv (contains eggs)"""
