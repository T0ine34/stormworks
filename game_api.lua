input = {
    getBool = function(index) return false end,
    getNumber = function(index) return 0 end
}

output = {
    setBool = function(index, value) end,
    setNumber = function(index, value) end
}

async = {
    httpGet = function(port, url) end
}

map = {
    mapToScreen = function(mapX, mapY, zoom, screenW, screenH, worldX, worldY) return 0, 0 end,
    screenToMap = function(mapX, mapY, zoom, screenW, screenH, pixelX, pixelY) return 0, 0 end
}

property = {
    getBool = function(label) return false end,
    getNumber = function(label) return 0 end,
    getText = function(label) return "" end
}

screen = {
    -- Screen Drawing Functions
    drawCircle = function(x, y, radius) end,
    drawCircleF = function(x, y, radius) end,
    drawClear = function() end,
    drawLine = function(x1, y1, x2, y2) end,
    drawMap = function(x, y, zoom) end,
    drawRect = function(x, y, width, height) end,
    drawRectF = function(x, y, width, height) end,
    drawText = function(x, y, text) end,
    drawTextBox = function(x, y, width, height, text, h_align, v_align) end,
    drawTriangle = function(x1, y1, x2, y2, x3, y3) end,
    drawTriangleF = function(x1, y1, x2, y2, x3, y3) end,

    -- Screen Properties,
    getHeight = function() return 0 end,
    getWidth = function() return 0 end,

    -- Screen Color Functions,
    setColor = function(r, g, b, a ) end,
    setMapColorGrass = function(r, g, b, a) end,
    setMapColorGravel = function(r, g, b, a) end,
    setMapColorLand = function(r, g, b, a) end,
    setMapColorOcean = function(r, g, b, a) end,
    setMapColorRock = function(r, g, b, a) end,
    setMapColorSand = function(r, g, b, a) end,
    setMapColorShallows = function(r, g, b, a) end,
    setMapColorSnow = function(r, g, b, a) end
}