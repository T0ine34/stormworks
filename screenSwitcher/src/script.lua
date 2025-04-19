-- made by Antoine Buirey

BUTTONS_Y = -2
CURRENT_BUTTON = 1
NB_BUTTONS = 4


function getButton_Y_tick()
    if BUTTONS_Y < 0 then
        BUTTONS_Y = input.getNumber(2) - 6
    end
    return BUTTONS_Y
end

function getButton_Y_draw()
    if BUTTONS_Y < 0 then
        BUTTONS_Y = screen.getHeight() - 6 -- set the button Y position to the bottom of the screen
    end
    return BUTTONS_Y
end

function getButtons_X()
    local buttonsX = {}
    for i = 0, NB_BUTTONS - 1 do
        local x = i * 8 + 2 -- calculate the x position of each button
        table.insert(buttonsX, x) -- add the x position to the buttonsX table
    end
    return buttonsX
end


function getClickCoords()
    local x = input.getNumber(3) -- X coordinate of the click
    local y = input.getNumber(4) -- Y coordinate of the click
    return x, y
end

function getButtonClicked(x, y)
    local buttonsX = getButtons_X()
    local buttonY = getButton_Y_tick()
    for i, buttonX in ipairs(buttonsX) do
        if x >= buttonX and x < buttonX + 4 and y >= buttonY and y < buttonY + 4 then
            return i -- return the index of the button clicked
        end
    end
    return nil -- no button clicked
end


function onTick()
    -- get the coordinates of the click
    local x, y = getClickCoords()
    -- check if a button was clicked
    local buttonClicked = getButtonClicked(x, y)
    if buttonClicked then
        -- do something with the button clicked
        CURRENT_BUTTON = buttonClicked -- update the current button
    end
    output.setNumber(1, CURRENT_BUTTON) -- set the output to the button clicked index
end


function drawButtons()
    local buttonsX = getButtons_X()
    local buttonY = getButton_Y_draw()
    for i, x in ipairs(buttonsX) do
        screen.setColor(127, 127, 127, 255) -- set color to grey
        if i == CURRENT_BUTTON then
            screen.setColor(255, 255, 255, 255) -- set color to white for the current button
        end
        -- draw a button at the position (x, y)
        screen.drawRectF(x, buttonY, 4, 4)
    end
end


function onDraw()
    -- draw the buttons on the screen
    drawButtons()
end
