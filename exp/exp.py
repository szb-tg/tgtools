import pyTigerGraph as tg
import json

def main():
    objects = []
    gen_ddl = True
    gen_job = True

    # Connecting to TG
    conn = tg.TigerGraphConnection(restppPort="30900", gsPort="30240", graphname="cja")
    vts = conn.getVertexTypes()
    ets = conn.getEdgeTypes()

    # Here will come the parsing of parameters, including glob expansion
    # By the end of this part, `vs` and `es` contain only valid object names
    vs = ["customer_journey"]
    es = ["ch2tp"]
    add_header = False

    sep = ","

    # if args.extension:
    #     ext = args.extension
    # else:
    ext = ".csv"
    if sep == "\t":
        ext = ".tsv"

    # Processing vertices
    if len(vs) > 0:
        print("-- VERTICES ----------------------------")
    for v in vs:
        print("Processing vertex " + v + "...")
        # Generate DDL
        if gen_ddl:
            pass

        vd = conn.getVertexType(v)
        # Get ID and attribute names
        idn = vd["PrimaryId"]["AttributeName"]
        ans = []
        for a in vd["Attributes"]:
            ans.append(a["AttributeName"])

        # Generating data file
        dfn = v + ext
        df = open(dfn, "w")

        if add_header:
            df.write(idn + sep + sep.join(ans) + "\n")

        # Get the data
        data = conn.getVertices(v)
        for d in data:
            out = [d["v_id"]]
            attrs = d["attributes"]
            for an in ans:
                if an != idn:
                    out.append(attrs[an])
            df.write(sep.join(out) + "\n")

        df.close()

        # Generate loading job file
        if gen_job:
            jf = open("load_" + v + ".gsql", "w")

            jf.write("USE GRAPH " + conn.graphname + "\n")
            jf.write("DROP JOB load_" + v + "\n")
            jf.write("BEGIN\nCREATE LOADING JOB load_" + v + " FOR GRAPH " + conn.graphname + " {\n")
            jf.write("    DEFINE FILENAME datafile = \"" + dfn + "\";\n")
            jf.write("    LOAD datafile TO VERTEX " + v + " VALUES (")
            if add_header:
                jf.write("$\"" + idn + "\"")
            else:
                jf.write("$0")
            num = 1
            for a in ans:
                jf.write(", ")
                if add_header:
                    jf.write("$\"" + a + "\"")
                else:
                    jf.write("$" + str(num))
                num += 1
            jf.write(") USING SEPARATOR=\"" + ("\\t" if sep == "\t" else sep) + "\"")
            if add_header:
                jf.write(", HEADER=\"true\"")
            jf.write(";\n")
            jf.write("}\nEND\n")

            jf.close()

    # Processing edges
    if len(es) > 0:
        print("-- EDGES -------------------------------")
    for e in es:
        print("Processing edge " + e + "...")


if __name__ == "__main__":
    main()
