import { parseBool, getCurrentLayout, strip, clamp, scale, parseInputMode } from "../../dist/front/utils.js";


describe("parseBool", () => {
    it("should parse true", () => {
        expect(parseBool(true)).toBe(true);
        expect(parseBool("true")).toBe(true);
        expect(parseBool("True")).toBe(true);
        expect(parseBool("TRUE")).toBe(true);
    });
    it("should parse false", () => {
        expect(parseBool(false)).toBe(false);
        expect(parseBool("false")).toBe(false);
        expect(parseBool("False")).toBe(false);
        expect(parseBool("FALSE")).toBe(false);
    });
    it("should throw on invalid input", () => {
        expect(() => parseBool("invalid")).toThrow();
    });
});



describe("getCurrentLayout", () => {
    let window = {
        location: {
            href: ""
        }
    };
    it("should return the current layout", () => {
        // @ts-ignore
        window.location.href = "http://localhost:8000/tests/client/utils.test.mjs";
        expect(getCurrentLayout(window)).toBe("utils");
    });
    it("should throw on invalid URL", () => {
        // @ts-ignore
        window.location.href = "http://localhost:8000/tests/client/";
        expect(() => getCurrentLayout(window)).toThrow();
    });
});


describe("strip", () => {
    it("should strip whitespace", () => {
        expect(strip("  test  ")).toBe("test");
    });
    it("should not strip non-whitespace", () => {
        expect(strip("test")).toBe("test");
    });
    it("should strip string with only whitespace chars", () => {
        expect(strip(" ")).toBe("");
    });
    it("should strip empty string", () => {
        expect(strip("")).toBe("");
    });
});


describe("clamp", () => {
    it("should clamp value", () => {
        expect(clamp(5, 0, 10)).toBe(5);
        expect(clamp(-5, 0, 10)).toBe(0);
        expect(clamp(15, 0, 10)).toBe(10);
    });
});


describe("scale", () => {
    it("should scale positive integer value", () => {
        expect(scale(5, 0, 10, 0, 100)).toBe(50);
        expect(scale(0, 0, 10, 0, 100)).toBe(0);
        expect(scale(10, 0, 10, 0, 100)).toBe(100);
    });
    it("should scale negative integer value", () => {
        expect(scale(-5, -10, 0, 0, 100)).toBe(50);
        expect(scale(-10, -10, 0, 0, 100)).toBe(0);
        expect(scale(0, -10, 0, 0, 100)).toBe(100);
    });
    it("should scale positive float value", () => {
        expect(scale(5.5, 0, 10, 0, 100)).toBeCloseTo(55);
        expect(scale(0.5, 0, 10, 0, 100)).toBeCloseTo(5);
        expect(scale(10.5, 0, 10, 0, 100)).toBeCloseTo(105);
    });
    it("should scale negative float value", () => {
        expect(scale(-5.5, -10, 0, 0, 100)).toBeCloseTo(45);
        expect(scale(-0.5, -10, 0, 0, 100)).toBeCloseTo(95);
        expect(scale(-9.5, -10, 0, 0, 100)).toBeCloseTo(5);
    });
});


describe("parseInputMode", () => {
    it("should parse input mode", () => {
        expect(parseInputMode("none")).toEqual({mode: "none", channel: ""});
        expect(parseInputMode("input:b1")).toEqual({mode: "input", channel: "b1"});
        expect(parseInputMode("output:n32")).toEqual({mode: "output", channel: "n32"});
    });
    it("should throw on invalid input mode", () => {
        expect(() => parseInputMode("invalid")).toThrow();
    });
});