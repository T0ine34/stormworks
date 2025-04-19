-- made by Antoine Buirey


MAX_MSG_LENGTH = 8

-- type of vehicles are:
-- 1: boat
-- 2: car
-- 3: helicopter
-- 4: plane

-- input channels
    -- number
        KEY_PRESSED_X_CHANNEL = 3
        KEY_PRESSED_Y_CHANNEL = 4
        FREQUENCY_CHANNEL = 7
        SIGNAL_STRENGTH_CHANNEL = 8

        TYPE_CHANNEL = 24
        -- channels numbers from 25 to 32 will be the letters of the message

    -- boolean
        KEY_PRESSED_CHANNEL = 1
        EMIT_CHANNEL = 7

-- output channels
    -- number

    -- boolean
        FREQUENCY_UP_CHANNEL = 1
        FREQUENCY_DOWN_CHANNEL = 2

function showError(msg)
    screen.setColor(255, 0, 0)
    screen.drawText(0, screen.getHeight() / 2 - 2, msg)
end


function encodeText(message) -- encode the message into a list of numbers, support all printable ASCII characters
    if #message > MAX_MSG_LENGTH then -- if the message is too long
        return
    end
    local encodedMessage = {0, 0, 0, 0, 0, 0, 0, 0}
    for i = 1, #message do
        local charCode = message:byte(i) -- get the ASCII code of the i-th character of the message
        if charCode < 32 or charCode > 126 then -- if the character is not a printable ASCII character
            return
        end
        encodedMessage[#encodedMessage + 1] = charCode -- add the ASCII code to the encoded message
    end
end


function decodeText(encodedText) -- decode the message from a list of numbers
    if #encodedText > MAX_MSG_LENGTH then -- if the message is too long
        return
    end
    local decodedMessage = ""
    for i = 1, #encodedText do
        local charCode = encodedText[i]
        if charCode == 0 then -- if the character is a null character
            break
        end
        if charCode < 32 or charCode > 126 then -- if the character is not a printable ASCII character
            return
        end
        decodedMessage = decodedMessage .. string.char(charCode) -- add the character to the decoded message
    end
    return decodedMessage
end


function sendText(text)
    local encodedText = encodeText(text)
    if encodedText == nil then
        return
    end
    for i = 1, #encodedText do
        local channel = i + 24 -- channels numbers from 24 to 32 will be the letters of the message
        output.setNumber(channel, encodedText[i])
    end
end

function readText()
    local encodedText = {}
    for i = 25, 32 do
        local charCode = input.getNumber(i)
        if charCode == nil then
            return ""
        end
        if charCode == 0 then
            break
        end
        if charCode < 32 or charCode > 126 then
            return "INVALID MESSAGE" .. charCode
        end
        encodedText[#encodedText + 1] = charCode
    end
    return decodeText(encodedText)
end


function onKeyPressed(x, y)
    if x > 5 and x < 15 and y > 2 and y < 7.5 then
        return {freqUp=true, freqDown=false}
    elseif x > 5 and x < 15 and y > 16.5 and y < 22 then
        return {freqUp=false, freqDown=true}
    end
    return {freqUp=false, freqDown=false}
end


TEXT = ""
EMIT = false
RECEIVE = false
FREQUENCY = 1
TYPE = 1

BTN_CLICKED = {freqUp=false, freqDown=false}

LAST_KEY_STATE = true

function onTick()
    EMIT = input.getBool(EMIT_CHANNEL)
    TEXT = readText()
    FREQUENCY = input.getNumber(FREQUENCY_CHANNEL)
    TYPE = input.getNumber(TYPE_CHANNEL)
    SIGNAL_STRENGTH = input.getNumber(SIGNAL_STRENGTH_CHANNEL)
    RECEIVE =  SIGNAL_STRENGTH > 0

    if input.getBool(KEY_PRESSED_CHANNEL) and not LAST_KEY_STATE then
        BTN_CLICKED = onKeyPressed(input.getNumber(KEY_PRESSED_X_CHANNEL), input.getNumber(KEY_PRESSED_Y_CHANNEL))
    else
        BTN_CLICKED = {freqUp=false, freqDown=false}
    end
    LAST_KEY_STATE = input.getBool(KEY_PRESSED_CHANNEL)

    output.setBool(FREQUENCY_UP_CHANNEL, BTN_CLICKED.freqUp)
    output.setBool(FREQUENCY_DOWN_CHANNEL, BTN_CLICKED.freqDown)
end

function drawUnknown(x, y)
    screen.setColor(127, 127, 127)
    screen.drawText(x-2, y-2, "?")
end

function drawBoat(x, y)
    -- a small ship icon facing top seen from above
    -- x, y is the center of the ship
    screen.setColor(127, 127, 127)
    screen.drawLine(x, y-5, x+2, y-1)
    screen.drawLine(x, y-5, x-2, y-1)
    screen.drawLine(x+2, y-1, x+2, y+5)
    screen.drawLine(x-2, y-1, x-2, y+5)
    screen.drawLine(x+2, y+5, x-2, y+5)
end

function drawCar(x, y)
    -- a small car icon facing right seen from the side
    -- x, y is the center of the car
    screen.setColor(127, 127, 127)
    screen.drawCircle(x-3, y+3, 1) -- wheels
    screen.drawCircle(x+3, y+3, 1)

    screen.drawLine(x-5, y+3, x-4, y+3) -- bottom
    screen.drawLine(x-2, y+3, x+2, y+3)
    screen.drawLine(x+4, y+3, x+5, y+3)
    
    screen.drawLine(x-5, y+3, x-5, y+1) -- rear
    screen.drawLine(x-5, y+1, x-3, y)
    screen.drawLine(x-3, y, x-2, y-1)

    screen.drawLine(x+5, y+3, x+5, y+1) -- front
    screen.drawLine(x+5, y+1, x+2, y)
    screen.drawLine(x+2, y, x+1, y-1)

    screen.drawLine(x-2, y-1, x+1, y-1) -- top
end

function drawHelicopter(x, y)
    -- a small helicopter icon facing right seen from the top
    -- x, y is the center of the helicopter
    screen.setColor(127, 127, 127)

    screen.drawLine(x, y-4, x, y+4)
    screen.drawLine(x-4, y, x+4, y)
    screen.drawLine(x-3, y-3, x+3, y+3)
    screen.drawLine(x-3, y+3, x+3, y-3)

    screen.drawRectF(x-1, y-1, 2, 4)
    screen.drawTriangleF(x-1, y+3, x+1, y+3, x, y+5)
    screen.drawCircleF(x, y-1, 1)
end

function drawPlane(x, y)
    -- a small plane icon facing right seen from the top
    -- x, y is the center of the plane
    screen.setColor(127, 127, 127)

    screen.drawLine(x, y-5, x-1, y-3)
    screen.drawLine(x, y-5, x+1, y-3)
    
    screen.drawLine(x-1, y-3, x-1, y-1)
    screen.drawLine(x+1, y-3, x+1, y-1)
    
    screen.drawLine(x+1, y-1, x+5, y)
    screen.drawLine(x+5, y, x+5, y+1)
    screen.drawLine(x+5, y+1, x+1, y+1)
    
    screen.drawLine(x-1, y-1, x-5, y)
    screen.drawLine(x-5, y, x-5, y+1)
    screen.drawLine(x-5, y+1, x-1, y+1)
    
    screen.drawLine(x+1, y+1, x+1, y+3)
    screen.drawLine(x-1, y+1, x-1, y+3)
    
    
    screen.drawLine(x+1, y+3, x+3, y+4)
    screen.drawLine(x-1, y+3, x-3, y+4)
    
    screen.drawLine(x+3, y+4, x+3, y+5)
    screen.drawLine(x-3, y+4, x-3, y+5)
    
    screen.drawLine(x+3, y+5, x, y+4)
    screen.drawLine(x-3, y+5, x, y+4)
end


function drawSender(senderName, senderType)
    screen.setColor(255, 255, 255)
    if senderName == "" then
        senderName = "Unknown"
    end
    screen.drawText(36, screen.getHeight()/4 - 2, senderName)
    if senderType == 0 then
        drawUnknown(29, screen.getHeight()/4)
    elseif senderType == 1 then
        drawBoat(29, screen.getHeight()/4)
    elseif senderType == 2 then
        drawCar(29, screen.getHeight()/4)
    elseif senderType == 3 then
        drawHelicopter(29, screen.getHeight()/4)
    elseif senderType == 4 then
        drawPlane(29, screen.getHeight()/4)
    end
end


function drawSignalStrength(strength) -- strength is between 0 and 1
    local colors = { -- 15 colors from red to green, going through yellow
    {255, 0, 0},
    {255, 51, 0},
    {255, 102, 0},
    {255, 153, 0},
    {255, 204, 0},
    {255, 255, 0},
    {204, 255, 0},
    {153, 255, 0},
    {102, 255, 0},
    {51, 255, 0},
    {0, 255, 0},
    {0, 204, 0},
    {0, 153, 0},
    {0, 102, 0},
    {0, 51, 0}
    }
    
    -- 15 vertical bars of colors from red to green, only the first strength*15 bars are drawn
    for i = 1, 15 do
        if i <= strength * 15 then
            screen.setColor(colors[i][1], colors[i][2], colors[i][3])
        else
            screen.setColor(16, 16, 16)
        end
        screen.drawRectF(29+(i*3), ((screen.getHeight()/4)*3)-4, 2, 8)
    end

end


function drawEmitCircle(isEmiting)
    if isEmiting then
        screen.setColor(255, 0, 0)
    else
        screen.setColor(32, 0, 0)
    end
    screen.drawCircleF(screen.getWidth() - 10, screen.getHeight()/2 + 10, 4)
end


function drawCommArrow(isEmiting, isReceiving)
    screen.setColor(255, 255, 255)
    if isEmiting or isReceiving then
        screen.drawLine(screen.getWidth() - 10, 2, screen.getWidth() - 10, screen.getHeight()/2)
    end
    if isEmiting then
        screen.drawLine(screen.getWidth() - 10, 2, screen.getWidth() - 5, 7)
        screen.drawLine(screen.getWidth() - 10, 2, screen.getWidth() - 15, 7)
    end
    if isReceiving then
        screen.drawLine(screen.getWidth() - 10, screen.getHeight()/2, screen.getWidth() - 5, screen.getHeight()/2 - 5)
        screen.drawLine(screen.getWidth() - 10, screen.getHeight()/2, screen.getWidth() - 15, screen.getHeight()/2 - 5)
    end
end


function drawFrequencySelector(frequency, up_clicked, down_clicked)
    screen.setColor(255, 255, 255)
    screen.drawText(5, 10, string.format("%02d", frequency))
    screen.drawText(1, 24, "freq")

    if up_clicked then
        screen.setColor(0, 255, 0)
    else
        screen.setColor(255, 255, 255)
    end
    screen.drawTriangleF(10, 2, 5, 7.5, 15, 7.5) -- plus button

    if down_clicked then
        screen.setColor(0, 255, 0)
    else
        screen.setColor(255, 255, 255)
    end
    screen.drawTriangleF(10, 22, 5, 16.5, 15, 16.5) -- minus button
end


function onDraw()
    local width = screen.getWidth()
    local height = screen.getHeight()

    if width ~= 96 or height ~= 32 then
        showError("Use a 3x1 screen")
        return
    end

    drawFrequencySelector(FREQUENCY, BTN_CLICKED.freqUp, BTN_CLICKED.freqDown)

    screen.setColor(255, 255, 255)
    screen.drawLine(22, 0, 22, height)

    drawEmitCircle(EMIT)
    drawCommArrow(EMIT, RECEIVE)

    if RECEIVE then
        drawSender(TEXT, TYPE)
        drawSignalStrength(SIGNAL_STRENGTH)
    end


end
