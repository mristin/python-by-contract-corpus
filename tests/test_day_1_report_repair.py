import unittest

from icontract_hypothesis import test_with_inferred_strategy

from aocdbc.day_1_report_repair import find_pair_with_sum
from aocdbc.day_1_report_repair import find_n_items_with_sum


class TestDay1(unittest.TestCase):
    def test_part_1(self) -> None:
        entries = list(map(int, _CHALLENGE_DATA.split()))
        ret = find_pair_with_sum(entries, 2020)
        assert ret is not None
        self.assertEqual(ret[0] * ret[1], 1016131)

    def test_part_2(self) -> None:
        entries = list(map(int, _CHALLENGE_DATA.split()))
        ret = find_n_items_with_sum(entries, 3, 2020)
        assert ret is not None
        self.assertEqual(ret[0] * ret[1] * ret[2], 276432018)

    def TODO_test_verify_with_icontract_hypothesis(self) -> None:
        test_with_inferred_strategy(find_pair_with_sum)

    def TODO_test_verify_line_with_icontract_hypothesis(self) -> None:
        test_with_inferred_strategy(find_n_items_with_sum)


_CHALLENGE_DATA = """
1895
1504
1660
1775
1743
1607
1267
1133
292
1646
1285
1808
1512
1839
1869
1578
1318
1385
1829
1800
1491
1600
1290
1856
1781
1881
1953
2008
1681
1472
1846
2010
1619
1584
1849
1876
1744
1980
1421
911
1308
1762
1398
1470
1974
1902
1985
2001
1926
1374
1678
1523
1894
1597
1778
1940
1362
1613
1629
1473
1633
1867
1838
1931
1850
1776
1689
1311
1947
1988
1779
1381
1683
1677
1675
1587
767
1401
1412
1544
1484
618
1755
1073
1970
1735
1770
1623
1665
1783
1400
1892
1921
1506
1978
1731
1739
1515
1354
1264
1394
1763
1569
1453
1539
2006
1586
1855
1609
1729
1624
506
1668
1803
1486
1767
1720
1753
1994
1718
1922
1314
1250
1516
1546
1625
1708
1286
1993
1785
491
1705
1924
1752
1888
1651
1604
1750
1547
1481
1704
1851
904
1920
1939
1277
1870
1934
1617
1833
1797
1817
1967
1935
1914
1621
1468
1859
1552
1640
1709
1121
1973
1343
1266
1806
1360
1299
1990
1356
1631
1555
1811
1323
1794
1550
1448
1848
1826
1723
1891
1302
1655
947
1580
1908
1641
1816
1701
1871
1588
1843
1643
1893
1866
1628
1417
1795
1995
1937
"""


if __name__ == "__main__":
    unittest.main()