import pyTigerGraph as tg
import TgMeta as tgm


def main():
    # conn = tg.TigerGraphConnection(host="http://127.0.0.1", restppPort="30900", gsPort="30240")
    conn = tg.TigerGraphConnection(host="http://127.0.0.1", restppPort="26900", gsPort="26240", gsqlVersion="2.6.0")
    # conn = tg.TigerGraphConnection(host="https://szba-buws.i.tgcloud.io", graphname="FraudGraph", useCert=True)
    # conn.debug=True
    # conn.getToken("accsjg1cfaqv9r2rodgn1eq976uo3hh1")

    meta = tgm.TgMeta(conn)

    res = meta.generateDDL()
    print("SET exit_on_error = FALSE")
    print("DROP ALL\n")
    for r in res:
        print("// " + "=" * 73)
        print("// " + r + "\n")

        first = True
        for s in res[r]:
            if r in ["LoadingJobs", "Queries"] and not first:
                print("// " + "-" * 73 + "\n")
            first = False
            if isinstance(s, list):
                for s2 in s:
                    print(s2)
                print()
            else:
                print(s + "\n")
    print("\n// EOF")


if __name__ == "__main__":
    main()

# EOF
