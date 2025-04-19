from stormworks_server.colors import Color

class TestColor:
    def test_fromHex(self):
        # with 6 digits format (RRGGBB)
        assert Color.fromHex("#000000") == Color(0, 0, 0)
        assert Color.fromHex("#ffffff") == Color(255, 255, 255)
        assert Color.fromHex("#0000ff") == Color(0, 0, 255)
        assert Color.fromHex("#00ff00") == Color(0, 255, 0)
        assert Color.fromHex("#ff0000") == Color(255, 0, 0)
        assert Color.fromHex("#ffff00") == Color(255, 255, 0)
        assert Color.fromHex("#ff00ff") == Color(255, 0, 255)
        assert Color.fromHex("#00ffff") == Color(0, 255, 255)
        assert Color.fromHex("#c8c837") == Color(200, 200, 55)
        assert Color.fromHex("#c8c838") == Color(200, 200, 56)
        assert Color.fromHex("#c8c8c8") == Color(200, 200, 200)

        # with 3 digits format (RGB)
        assert Color.fromHex("#000") == Color(0, 0, 0)
        assert Color.fromHex("#fff") == Color(255, 255, 255)
        assert Color.fromHex("#00f") == Color(0, 0, 255)
        assert Color.fromHex("#0f0") == Color(0, 255, 0)
        assert Color.fromHex("#f00") == Color(255, 0, 0)
        assert Color.fromHex("#ff0") == Color(255, 255, 0)
        assert Color.fromHex("#f0f") == Color(255, 0, 255)
        assert Color.fromHex("#0ff") == Color(0, 255, 255)
        assert Color.fromHex("#c87") == Color(204, 136, 119)
        assert Color.fromHex("#c88") == Color(204, 136, 136)
        assert Color.fromHex("#ccc") == Color(204, 204, 204)

        # with 8 digits format (RRGGBBAA)
        assert Color.fromHex("#00000000") == Color(0, 0, 0, 0)
        assert Color.fromHex("#ffffffff") == Color(255, 255, 255, 255)
        assert Color.fromHex("#0000ff00") == Color(0, 0, 255, 0)
        assert Color.fromHex("#00ff0000") == Color(0, 255, 0, 0)
        assert Color.fromHex("#ff000000") == Color(255, 0, 0, 0)
        assert Color.fromHex("#ffff0000") == Color(255, 255, 0, 0)
        assert Color.fromHex("#ff00ff00") == Color(255, 0, 255, 0)
        assert Color.fromHex("#00ffff00") == Color(0, 255, 255, 0)
        assert Color.fromHex("#c8c83700") == Color(200, 200, 55, 0)
        assert Color.fromHex("#c8c83800") == Color(200, 200, 56, 0)
        assert Color.fromHex("#c8c8c800") == Color(200, 200, 200, 0)

        # with 4 digits format (RGBA)
        assert Color.fromHex("#0000") == Color(0, 0, 0, 0)
        assert Color.fromHex("#ffff") == Color(255, 255, 255, 255)
        assert Color.fromHex("#00ff") == Color(0, 0, 255, 255)
        assert Color.fromHex("#0f00") == Color(0, 255, 0, 0)
        assert Color.fromHex("#f000") == Color(255, 0, 0, 0)
        assert Color.fromHex("#ff00") == Color(255, 255, 0, 0)
        assert Color.fromHex("#f0f0") == Color(255, 0, 255, 0)
        assert Color.fromHex("#0ff0") == Color(0, 255, 255, 0)
        assert Color.fromHex("#c87f") == Color(204, 136, 119, 255)
        assert Color.fromHex("#c88f") == Color(204, 136, 136, 255)
        assert Color.fromHex("#cccf") == Color(204, 204, 204, 255)

    def test_fromRgb(self):
        # 3 values format (RGB)
        assert Color.fromRgb("0, 0, 0") == Color(0, 0, 0)
        assert Color.fromRgb("255, 255, 255") == Color(255, 255, 255)
        assert Color.fromRgb("0, 0, 255") == Color(0, 0, 255)
        assert Color.fromRgb("0, 255, 0") == Color(0, 255, 0)
        assert Color.fromRgb("255, 0, 0") == Color(255, 0, 0)
        assert Color.fromRgb("255, 255, 0") == Color(255, 255, 0)
        assert Color.fromRgb("255, 0, 255") == Color(255, 0, 255)
        assert Color.fromRgb("0, 255, 255") == Color(0, 255, 255)
        assert Color.fromRgb("200, 200, 55") == Color(200, 200, 55)
        assert Color.fromRgb("200, 200, 56") == Color(200, 200, 56)
        assert Color.fromRgb("200, 200, 200") == Color(200, 200, 200)

        # 4 values format (RGBA)
        assert Color.fromRgb("0, 0, 0, 0") == Color(0, 0, 0, 0)
        assert Color.fromRgb("255, 255, 255, 255") == Color(255, 255, 255, 255)
        assert Color.fromRgb("0, 0, 255, 0") == Color(0, 0, 255, 0)
        assert Color.fromRgb("0, 255, 0, 0") == Color(0, 255, 0, 0)
        assert Color.fromRgb("255, 0, 0, 0") == Color(255, 0, 0, 0)
        assert Color.fromRgb("255, 255, 0, 0") == Color(255, 255, 0, 0)
        assert Color.fromRgb("255, 0, 255, 0") == Color(255, 0, 255, 0)
        assert Color.fromRgb("0, 255, 255, 0") == Color(0, 255, 255, 0)
        assert Color.fromRgb("200, 200, 55, 0") == Color(200, 200, 55, 0)
        assert Color.fromRgb("200, 200, 56, 0") == Color(200, 200, 56, 0)
        assert Color.fromRgb("200, 200, 200, 0") == Color(200, 200, 200, 0)

    def test_fromAuto(self):
        assert Color.fromAuto("#000000") == Color(0, 0, 0)
        assert Color.fromAuto("rgb(0, 0, 0)") == Color(0, 0, 0)
        assert Color.fromAuto("0, 0, 0") == Color(0, 0, 0)
        assert Color.fromAuto("rgba(0, 0, 0, 0)") == Color(0, 0, 0, 0)
        assert Color.fromAuto("0, 0, 0, 0") == Color(0, 0, 0, 0)
        assert Color.fromAuto("#ffffff") == Color(255, 255, 255)

    def test_str(self):
        assert str(Color(0, 0, 0)) == "rgba(0, 0, 0, 255)"
        assert str(Color(255, 255, 255)) == "rgba(255, 255, 255, 255)"
        assert str(Color(0, 0, 255)) == "rgba(0, 0, 255, 255)"
        assert str(Color(0, 255, 0)) == "rgba(0, 255, 0, 255)"
        assert str(Color(255, 0, 0)) == "rgba(255, 0, 0, 255)"
        assert str(Color(255, 255, 0)) == "rgba(255, 255, 0, 255)"
        assert str(Color(255, 0, 255)) == "rgba(255, 0, 255, 255)"
        assert str(Color(0, 255, 255)) == "rgba(0, 255, 255, 255)"
        assert str(Color(200, 200, 55)) == "rgba(200, 200, 55, 255)"
        assert str(Color(200, 200, 56, 0)) == "rgba(200, 200, 56, 0)"
        assert str(Color(200, 200, 200, 200)) == "rgba(200, 200, 200, 200)"

    def test_opposite(self):
        assert Color(0, 0, 0).opposite() == Color(255, 255, 255)
        assert Color(255, 255, 255).opposite() == Color(0, 0, 0)
        assert Color(0, 0, 255).opposite() == Color(255, 255, 0)
        assert Color(0, 255, 0).opposite() == Color(255, 0, 255)
        assert Color(255, 0, 0).opposite() == Color(0, 255, 255)
        assert Color(255, 255, 0).opposite() == Color(0, 0, 255)
        assert Color(255, 0, 255).opposite() == Color(0, 255, 0)
        assert Color(0, 255, 255).opposite() == Color(255, 0, 0)
        assert Color(200, 200, 55).opposite() == Color(55, 55, 200)
        assert Color(200, 200, 56).opposite() == Color(55, 55, 199)
        assert Color(200, 200, 200).opposite() == Color(55, 55, 55)

    def test_grayshade(self):
        assert Color(0, 0, 0).grayshade() == Color(0, 0, 0)
        assert Color(255, 255, 255).grayshade() == Color(255, 255, 255)
        assert Color(0, 0, 255).grayshade() == Color(29, 29, 29)
        assert Color(0, 255, 0).grayshade() == Color(150, 150, 150)
        assert Color(255, 0, 0).grayshade() == Color(76, 76, 76)
        assert Color(255, 255, 0).grayshade() == Color(226, 226, 226)
        assert Color(255, 0, 255).grayshade() == Color(105, 105, 105)
        assert Color(0, 255, 255).grayshade() == Color(179, 179, 179)
        assert Color(200, 200, 55).grayshade() == Color(183, 183, 183)
        assert Color(200, 200, 56).grayshade() == Color(184, 184, 184)
        assert Color(200, 200, 200).grayshade() == Color(200, 200, 200)

    def test_blackOrWhite(self):
        assert Color(0, 0, 0).blackOrWhite() == Color(0, 0, 0)
        assert Color(255, 255, 255).blackOrWhite() == Color(255, 255, 255)
        assert Color(0, 0, 255).blackOrWhite() == Color(0, 0, 0)
        assert Color(0, 255, 0).blackOrWhite() == Color(0, 0, 0)
        assert Color(255, 0, 0).blackOrWhite() == Color(0, 0, 0)
        assert Color(255, 255, 0).blackOrWhite() == Color(0, 0, 0)
        assert Color(255, 0, 255).blackOrWhite() == Color(0, 0, 0)
        assert Color(0, 255, 255).blackOrWhite() == Color(0, 0, 0)
        assert Color(200, 200, 55).blackOrWhite() == Color(255, 255, 255)
        assert Color(200, 200, 56).blackOrWhite() == Color(255, 255, 255)
        assert Color(200, 200, 200).blackOrWhite() == Color(255, 255, 255)

    def test_hex(self):
        assert Color(0, 0, 0).hex() == "#000000ff"
        assert Color(255, 255, 255).hex() == "#ffffffff"
        assert Color(0, 0, 255).hex() == "#0000ffff"
        assert Color(0, 255, 0).hex() == "#00ff00ff"
        assert Color(255, 0, 0).hex() == "#ff0000ff"
        assert Color(255, 255, 0).hex() == "#ffff00ff"
        assert Color(255, 0, 255).hex() == "#ff00ffff"
        assert Color(0, 255, 255).hex() == "#00ffffff"
        assert Color(200, 200, 55).hex() == "#c8c837ff"
        assert Color(200, 200, 56).hex() == "#c8c838ff"
        assert Color(200, 200, 200).hex() == "#c8c8c8ff"

    def test_rgb(self):
        assert Color(0, 0, 0).rgb() == "rgb(0, 0, 0)"
        assert Color(255, 255, 255).rgb() == "rgb(255, 255, 255)"
        assert Color(0, 0, 255).rgb() == "rgb(0, 0, 255)"
        assert Color(0, 255, 0).rgb() == "rgb(0, 255, 0)"
        assert Color(255, 0, 0).rgb() == "rgb(255, 0, 0)"
        assert Color(255, 255, 0).rgb() == "rgb(255, 255, 0)"
        assert Color(255, 0, 255).rgb() == "rgb(255, 0, 255)"
        assert Color(0, 255, 255).rgb() == "rgb(0, 255, 255)"
        assert Color(200, 200, 55).rgb() == "rgb(200, 200, 55)"
        assert Color(200, 200, 56).rgb() == "rgb(200, 200, 56)"
        assert Color(200, 200, 200).rgb() == "rgb(200, 200, 200)"

    def test_rgba(self):
        assert Color(0, 0, 0).rgba() == "rgba(0, 0, 0, 255)"
        assert Color(255, 255, 255).rgba() == "rgba(255, 255, 255, 255)"
        assert Color(0, 0, 255).rgba() == "rgba(0, 0, 255, 255)"
        assert Color(0, 255, 0).rgba() == "rgba(0, 255, 0, 255)"
        assert Color(255, 0, 0).rgba() == "rgba(255, 0, 0, 255)"
        assert Color(255, 255, 0).rgba() == "rgba(255, 255, 0, 255)"
        assert Color(255, 0, 255).rgba() == "rgba(255, 0, 255, 255)"
        assert Color(0, 255, 255).rgba() == "rgba(0, 255, 255, 255)"
        assert Color(200, 200, 55).rgba() == "rgba(200, 200, 55, 255)"
        assert Color(200, 200, 56).rgba() == "rgba(200, 200, 56, 255)"
        assert Color(200, 200, 200).rgba() == "rgba(200, 200, 200, 255)"

    def test_eq(self):
        assert Color(0, 0, 0) == Color(0, 0, 0)
        assert Color(255, 255, 255) == Color(255, 255, 255)
        assert Color(0, 0, 255) == Color(0, 0, 255)
        assert Color(0, 255, 0) == Color(0, 255, 0)
        assert Color(255, 0, 0) == Color(255, 0, 0)
        assert Color(255, 255, 0) == Color(255, 255, 0)
        assert Color(255, 0, 255) == Color(255, 0, 255)
        assert Color(0, 255, 255) == Color(0, 255, 255)
        assert Color(200, 200, 55) == Color(200, 200, 55)
        assert Color(200, 200, 56) == Color(200, 200, 56)
        assert Color(200, 200, 200) == Color(200, 200, 200)

    def test_ne(self):
        assert Color(0, 0, 0) != Color(255, 255, 255)
        assert Color(255, 255, 255) != Color(0, 0, 255)
        assert Color(0, 0, 255) != Color(0, 255, 0)
        assert Color(0, 255, 0) != Color(255, 0, 0)
        assert Color(255, 0, 0) != Color(255, 255, 0)
        assert Color(255, 255, 0) != Color(255, 0, 255)
        assert Color(255, 0, 255) != Color(0, 255, 255)
        assert Color(0, 255, 255) != Color(200, 200, 55)
        assert Color(200, 200, 55) != Color(200, 200, 56)
        assert Color(200, 200, 56) != Color(200, 200, 200)

    def test_add(self):
        assert Color(0, 0, 0) + Color(0, 0, 0) == Color(0, 0, 0)
        assert Color(255, 255, 255) + Color(255, 255, 255) == Color(255, 255, 255)
        assert Color(0, 0, 255) + Color(0, 0, 255) == Color(0, 0, 255)
        assert Color(0, 255, 0) + Color(0, 255, 0) == Color(0, 255, 0)
        assert Color(255, 0, 0) + Color(255, 0, 0) == Color(255, 0, 0)
        assert Color(255, 255, 0) + Color(255, 255, 0) == Color(255, 255, 0)
        assert Color(255, 0, 255) + Color(255, 0, 255) == Color(255, 0, 255)
        assert Color(0, 255, 255) + Color(0, 255, 255) == Color(0, 255, 255)
        assert Color(200, 200, 55) + Color(200, 200, 55) == Color(255, 255, 110)
        assert Color(200, 200, 56) + Color(200, 200, 56) == Color(255, 255, 112)
        assert Color(200, 200, 200) + Color(200, 200, 200) == Color(255, 255, 255)

    def test_sub(self):
        assert Color(0, 0, 0) - Color(0, 0, 0) == Color(0, 0, 0, 0)
        assert Color(255, 255, 255) - Color(0, 0, 0, 0) == Color(255, 255, 255, 255)
        assert Color(0, 0, 255) - Color(0, 0, 255) == Color(0, 0, 0, 0)
        assert Color(0, 128, 0) - Color(0, 28, 0, 0) == Color(0, 100, 0, 255)
        assert Color(255, 0, 0) - Color(255, 0, 0) == Color(0, 0, 0, 0)
