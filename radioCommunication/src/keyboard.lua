-- made by Antoine Buirey


MAX_MSG_LENGTH = 8

-- input channels
    -- number
        KEY_PRESSED_X_CHANNEL = 3
        KEY_PRESSED_Y_CHANNEL = 4

        -- channels numbers from 25 to 32 will be the letters of the message

    -- boolean
        KEY_PRESSED_CHANNEL = 1

-- output channels
    -- number
        -- channels numbers from 25 to 32 will be the letters of the message

    -- boolean
        UPDATE_MEMORIES_CHANNEL = 1

function showError(msg)
    screen.setColor(255, 0, 0)
    screen.drawText(0, screen.getHeight() / 2 - 2, msg)
end


function encodeText(message) -- encode the message into a list of numbers, support all printable ASCII characters
    if #message > MAX_MSG_LENGTH then -- if the message is too long
        return
    end
    local encodedMessage = {}
    for i = 1, #message do
        local charCode = message:byte(i) -- get the ASCII code of the i-th character of the message
        if charCode < 32 or charCode > 126 then -- if the character is not a printable ASCII character
            return
        end
        encodedMessage[#encodedMessage + 1] = charCode -- add the ASCII code to the encoded message
    end
    return encodedMessage
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
    -- put all the remaining channels to 0
    for i = #encodedText + 1, MAX_MSG_LENGTH do
        output.setNumber(i + 24, 0)
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



KEY_ZONES = { -- top-left corner and bottom-right corner of each key
        A={x1=3,  y1=7,  x2=8,  y2=13},
        B={x1=10, y1=7,  x2=15, y2=13},
        C={x1=17, y1=7,  x2=22, y2=13},
        D={x1=24, y1=7,  x2=29, y2=13},
        E={x1=31, y1=7,  x2=36, y2=13},
        F={x1=38, y1=7,  x2=43, y2=13},
        G={x1=45, y1=7,  x2=50, y2=13},
        H={x1=52, y1=7,  x2=57, y2=13},
        I={x1=59, y1=7,  x2=64, y2=13},
        J={x1=66, y1=7,  x2=71, y2=13},
        K={x1=73, y1=7,  x2=78, y2=13},
        L={x1=80, y1=7,  x2=85, y2=13},
        M={x1=87, y1=7,  x2=92, y2=13},
        N={x1=3,  y1=15, x2=8,  y2=21},
        O={x1=10, y1=15, x2=15, y2=21},
        P={x1=17, y1=15, x2=22, y2=21},
        Q={x1=24, y1=15, x2=29, y2=21},
        R={x1=31, y1=15, x2=36, y2=21},
        S={x1=38, y1=15, x2=43, y2=21},
        T={x1=45, y1=15, x2=50, y2=21},
        U={x1=52, y1=15, x2=57, y2=21},
        V={x1=59, y1=15, x2=64, y2=21},
        W={x1=66, y1=15, x2=71, y2=21},
        X={x1=73, y1=15, x2=78, y2=21},
        Y={x1=80, y1=15, x2=85, y2=21},
        Z={x1=87, y1=15, x2=92, y2=21},
    ["0"]={x1=3,  y1=23, x2=8 , y2=29},
    ["1"]={x1=10, y1=23, x2=15, y2=29},
    ["2"]={x1=17, y1=23, x2=22, y2=29},
    ["3"]={x1=24, y1=23, x2=29, y2=29},
    ["4"]={x1=31, y1=23, x2=36, y2=29},
    ["5"]={x1=38, y1=23, x2=43, y2=29},
    ["6"]={x1=45, y1=23, x2=50, y2=29},
    ["7"]={x1=52, y1=23, x2=57, y2=29},
    ["8"]={x1=59, y1=23, x2=64, y2=29},
    ["9"]={x1=66, y1=23, x2=71, y2=29},
    [" "]={x1=73, y1=23, x2=92, y2=29},
   DELETE={x1=80, y1=1,  x2=92, y2=7}
}

function onKeyPressed(x, y, text)
    for key, zone in pairs(KEY_ZONES) do
        if x > zone.x1 and x < zone.x2 and y > zone.y1 and y < zone.y2 then
            if key == "DELETE" then
                text = text:sub(1, -2) -- remove the last character
            elseif #text < MAX_MSG_LENGTH then
                text = text .. key
            end
            break
        end
    end
    return text
end

TEXT = ""

LAST_KEY_STATE = true

function onTick()
    if TEXT == "" then
        TEXT = readText()
    end

    if input.getBool(KEY_PRESSED_CHANNEL) and not LAST_KEY_STATE then
        TEXT = onKeyPressed(input.getNumber(KEY_PRESSED_X_CHANNEL), input.getNumber(KEY_PRESSED_Y_CHANNEL), TEXT)
    end
    LAST_KEY_STATE = input.getBool(KEY_PRESSED_CHANNEL)

    sendText(TEXT)
    output.setBool(UPDATE_MEMORIES_CHANNEL, true)
end


function drawText(x, y, text)
    screen.setColor(255, 255, 255)
    screen.drawText(x, y, text)
end


function drawKey(x, y, letter)
    screen.setColor(16, 16 ,16)
    screen.drawRectF(x, y, 6, 7)
    screen.setColor(255, 255, 255)
    screen.drawText(x + 1, y + 1, letter)
end

function drawSpaceBar(x, y)
    screen.setColor(16, 16 ,16)
    screen.drawRectF(x, y, 20, 7)
    screen.setColor(255, 255, 255)
    screen.drawLine(x + 2, y +6, x + 18, y + 6)
end

function drawDeleteButton(x, y)
    screen.setColor(16, 16 ,16)
    screen.drawRectF(x, y, 13, 6)
    screen.setColor(255, 255, 255)
    screen.drawLine(x + 2, y + 3, x + 11, y + 3)
    screen.drawLine(x + 2, y + 3, x + 4, y + 1)
    screen.drawLine(x + 2, y + 3, x + 4, y + 5)
end


function onDraw()
    local width = screen.getWidth()
    local height = screen.getHeight()

    if width ~= 96 or height ~= 32 then
        showError("Use a 3x1 screen")
        return
    end

    local firstRowY = 8
    local secondRowY = 16
    local thirdRowY = 24

                                                                            -- delete   confirm
    local firstRowKeys =  {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"}
    local secondRowKeys = {"N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"}
    local thirdRowKeys =  {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"} -- space here

    local function drawRowKeys(y, keys)
        for i, key in ipairs(keys) do
            drawKey(3 + (i - 1) * 7, y, key)
        end
    end

    drawRowKeys(firstRowY, firstRowKeys)
    drawRowKeys(secondRowY, secondRowKeys)
    drawRowKeys(thirdRowY, thirdRowKeys)

    drawSpaceBar(73, thirdRowY)
    drawDeleteButton(80, 1)

    drawText(1, 1, TEXT)
end
