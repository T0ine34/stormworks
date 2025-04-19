-- made by Antoine Buirey

-- one menu per group; only one of each group can be active at the same time (can be none)
-- the number is the channel on whitch the state of the button will be sent
LIGHT_GROUPS = {
    Restriction = {
        Restricted_by_draft = 7,
        Restricted_maneuverability = 3,
        No_control = 4,
        Mine_clearance = 14,
    },
    Movement_status = {
        In_movement = 2,
        Anchored = 5,
        Towed = 6
    },
    Activity = {
        Is_pilot = 10,
        Towing_above_200m = 9,
        Towing_below_200m = 8,
        Towing_alongside = 13
    },
    Obstruction = {
        Obstruction_on_left = 11,
        Obstruction_on_right = 12,
    },
    Interior = {
        White = 16,
        Red = 17,
        Auto = 18
    }
}

LABELS = { -- display names for each button
    Restricted_by_draft =           "DRAFT",
    Restricted_maneuverability =    "MANEUVER",
    No_control =                    "NO CONTROL",
    Mine_clearance =                "MINESWEEPER",
    In_movement =                   "MOVING",
    Anchored =                      "ANCHORED",
    Towed =                         "TOWED",
    Is_pilot =                      "PILOT",
    Towing_above_200m =             "TOWING >200m",
    Towing_below_200m =             "TOWING <200m",
    Towing_alongside =              "TOWING SIDE",
    Obstruction_on_left =           "LEFT",
    Obstruction_on_right =          "RIGHT",

    Restriction =                   "RESTRICTION",
    Movement_status =               "MOVEMENT",
    Activity =                      "ACTIVITY",
    Obstruction =                   "OBSTRUCTION",

    Interior =                      "INTERIOR",
    White =                         "WHITE",
    Red =                           "RED",
    Auto =                          "AUTO",
}



CURRENT_MENU = "main"

-- default values, by group
CURRENT_OPTIONS = {
    Restriction = nil,
    Movement_status = nil,
    Activity = nil,
    Obstruction = nil,
    -- interior lights are on auto by default
    Interior = LIGHT_GROUPS.Interior.Auto
}

-- locked options, by group (if true, all components of the group are locked)
LOCKED_OPTIONS = {
    Restriction = false,
    Movement_status = false,
    Activity = false,
    Obstruction = false,
    Interior = false
}



function onClick(x, y)
    if CURRENT_MENU == "main" then
        local i = 0
        for key, value in pairs(LIGHT_GROUPS) do
            if y >= i * 15 and y < (i + 1) * 15 then
                CURRENT_MENU = key
                break
            end
            i = i + 1
        end
    else
        if y >= input.getNumber(2) - 15 then
            CURRENT_MENU = "main"
        else
            local i = 0
            for key, value in pairs(LIGHT_GROUPS[CURRENT_MENU]) do
                if y >= i * 15 and y < (i + 1) * 15 then
                    if CURRENT_OPTIONS[CURRENT_MENU] == value then
                        CURRENT_OPTIONS[CURRENT_MENU] = nil
                    else
                        CURRENT_OPTIONS[CURRENT_MENU] = value
                    end
                    break
                end
                i = i + 1
            end
        end
    end
end

function SetGroupOutputs(group)
    for key, value in pairs(LIGHT_GROUPS[group]) do
        if CURRENT_OPTIONS[group] == value then
            output.setBool(value, true)
        else
            output.setBool(value, false)
        end
    end
end


LAST_CLICK_STATE = false

function onTick()
    if input.getBool(1) and not LAST_CLICK_STATE then
        LAST_CLICK_STATE = true
        onClick(input.getNumber(3), input.getNumber(4))
    elseif not input.getBool(1) then
        LAST_CLICK_STATE = false
    end

    if CURRENT_OPTIONS["Activity"] == LIGHT_GROUPS.Activity.Towing_above_200m         -- Towing above 200m
    or CURRENT_OPTIONS["Activity"] == LIGHT_GROUPS.Activity.Towing_below_200m         -- Towing below 200m
    or CURRENT_OPTIONS["Activity"] == LIGHT_GROUPS.Activity.Towing_alongside then     -- Towing alongside
        CURRENT_OPTIONS["Movement_status"] = LIGHT_GROUPS.Movement_status.In_movement
        LOCKED_OPTIONS["Movement_status"] = true
    else
        LOCKED_OPTIONS["Movement_status"] = false
    end

    for key, value in pairs(LIGHT_GROUPS) do
        SetGroupOutputs(key)
    end
end


function drawButton(x, y, width, text, color, textColor)
    screen.setColor(color[1], color[2], color[3])
    screen.drawRectF(x, y, width-1, 15)
    screen.setColor(255, 255, 255)
    screen.drawRect(x, y, width-1, 15)
    screen.setColor(textColor[1], textColor[2], textColor[3])
    screen.drawText(x + 2, y + 5, text)
end

function drawMenu(x, y, width, group)
    local i = 0
    for key, value in pairs(LIGHT_GROUPS[group]) do
        if CURRENT_OPTIONS[group] == value and LOCKED_OPTIONS[group] then
            color = {127, 0, 0}
            textColor = {255, 255, 255}
        elseif CURRENT_OPTIONS[group] == value and not LOCKED_OPTIONS[group] then
            color = {255, 127, 127}
            textColor = {0, 0, 0}
        elseif CURRENT_OPTIONS[group] ~= value and LOCKED_OPTIONS[group] then
            color = {127, 127, 127}
            textColor = {255, 255, 255}
        else
            color = {0, 0, 0}
            textColor = {255, 255, 255}
        end
        drawButton(x, y + i * 15, width, LABELS[key], color, textColor)
        i = i + 1
    end
end

function drawBackButton(x, y, width)
    drawButton(x, y, width, "BACK", {0, 0, 0}, {255, 255, 255})
end

function drawMainMenu()
    local x = 0
    local y = 0
    local width = screen.getWidth()
    for key, value in pairs(LIGHT_GROUPS) do
        drawButton(x, y, width, LABELS[key], {0, 0, 0}, {255, 255, 255})
        y = y + 15
    end
end

function onDraw()
    screen.setColor(0, 0, 0)
    screen.drawClear()
    screen.setColor(255, 255, 255)
    if CURRENT_MENU == "main" then
        drawMainMenu()
    else
        drawMenu(0, 0, screen.getWidth(), CURRENT_MENU)
        drawBackButton(0, screen.getHeight() - 16, screen.getWidth())
    end
end
