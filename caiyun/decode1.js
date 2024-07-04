function decode1(input) {
    o=String.fromCharCode;
    function wt(e) {
        const i = ot(e);
        return at(i)
    }

    function ot(e) {
        const i = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
            , n = "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm"
            , u = s => i.indexOf(s)
            , r = s => u(s) > -1 ? n[u(s)] : s;
        return e.split("").map(r).join("")
    }

    function at(e) {
        return b(e)
    }

    b = function (t) {
        return N(D(t))
    }
    D = function (t) {
        return String(t).replace(/[-_]/g, function (a) {
            return a == "-" ? "+" : "/"
        }).replace(/[^A-Za-z0-9\+\/]/g, "")
    }
    N = function (t) {
        return R(z(t))
    }
    z = function (t) {
        return atob(t)
    }
    R = function (t) {
        var I = /[\xC0-\xDF][\x80-\xBF]|[\xE0-\xEF][\x80-\xBF]{2}|[\xF0-\xF7][\x80-\xBF]{3}/g
        return t.replace(I, P)
    }
    P = function (t) {
        switch (t.length) {
            case 4:
                var a = (7 & t.charCodeAt(0)) << 18 | (63 & t.charCodeAt(1)) << 12 | (63 & t.charCodeAt(2)) << 6 | 63 & t.charCodeAt(3)
                    , c = a - 65536;
                return o((c >>> 10) + 55296) + o((c & 1023) + 56320);
            case 3:
                return o((15 & t.charCodeAt(0)) << 12 | (63 & t.charCodeAt(1)) << 6 | 63 & t.charCodeAt(2));
            default:
                return o((31 & t.charCodeAt(0)) << 6 | 63 & t.charCodeAt(1))
        }
    }
    return wt(input)
}