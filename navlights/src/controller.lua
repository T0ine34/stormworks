-- made by Antoine Buirey



INPUTS = { --boolean inputs
    Restricted_by_draft = 7,
    Restricted_maneuverability = 3,
    No_control = 4,
    Mine_clearance = 14,
    In_movement = 2,
    Anchored = 5,
    Towed = 6,
    Is_pilot = 10,
    Towing_above_200m = 9,
    Towing_below_200m = 8,
    Towing_alongside = 13,
    Obstruction_on_left = 11,
    Obstruction_on_right = 12,
}



COLORS = {
    RED = {255, 0, 0},
    GREEN = {0, 255, 0},
    YELLOW = {255, 255, 0},
    WHITE = {255, 255, 255},
    OFF = {0, 0, 0}
}

TYPES = {
    RGB = 1,
    STANDARD = 2,
    UNUSED = 3
}


LIGHT_TYPES = {
    front_mast_3 = TYPES.RGB,
    front_mast_2 = TYPES.RGB,
    front_mast_1 = TYPES.RGB,
    middle_mast_3 = TYPES.RGB,
    middle_mast_2 = TYPES.RGB,
    middle_mast_1 = TYPES.RGB,
    rear_light_top = TYPES.STANDARD,
    rear_light_bottom = TYPES.STANDARD,
    left_light = TYPES.STANDARD,
    right_light = TYPES.STANDARD,
    minesweeper_left_light = TYPES.STANDARD,
    minesweeper_right_light = TYPES.STANDARD,
    minesweeper_light = TYPES.STANDARD,
    Obstruction_left_top = TYPES.RGB,
    Obstruction_left_bottom = TYPES.RGB,
    Obstruction_right_top = TYPES.RGB,
    Obstruction_right_bottom = TYPES.RGB
}

LIGHTS_STATUS = {
    front_mast_3 = COLORS.OFF,
    front_mast_2 = COLORS.OFF,
    front_mast_1 = COLORS.OFF,
    middle_mast_3 = COLORS.OFF,
    middle_mast_2 = COLORS.OFF,
    middle_mast_1 = COLORS.OFF,
    rear_light_top = false,
    rear_light_bottom = false,
    left_light = false,
    right_light = false,
    minesweeper_left_light = false,
    minesweeper_right_light = false,
    minesweeper_light = false,
    Obstruction_left_top = COLORS.OFF,
    Obstruction_left_bottom = COLORS.OFF,
    Obstruction_right_top = COLORS.OFF,
    Obstruction_right_bottom = COLORS.OFF
}

LIGHTS_COLORS = { -- colors of standard lights
    rear_light_top = COLORS.YELLOW,
    rear_light_bottom = COLORS.WHITE,
    left_light = COLORS.RED,
    right_light = COLORS.GREEN,
    minesweeper_left_light = COLORS.GREEN,
    minesweeper_right_light = COLORS.GREEN,
    minesweeper_light = COLORS.GREEN
}

LIGHTS_CHANNELS = {
    front_mast_3 = {1, 2, 3},               -- RGB
    front_mast_2 = {4, 5, 6},               -- RGB
    front_mast_1 = {7, 8, 9},               -- RGB
    middle_mast_3 = {10, 11, 12},           -- RGB
    middle_mast_2 = {13, 14, 15},           -- RGB
    middle_mast_1 = {16, 17, 18},           -- RGB
    rear_light_top = 1,                     -- on/off
    rear_light_bottom = 2,                  -- on/off
    left_light = 3,                         -- on/off
    right_light = nil,                      -- on/off (same channel as left_light)
    minesweeper_light = 4,                  -- on/off
    minesweeper_left_light = nil,           -- on/off (same channel as minesweeper_light)
    minesweeper_right_light = nil,          -- on/off (same channel as minesweeper_light)
    Obstruction_left_top = {19, 20, 21},    -- RGB
    Obstruction_left_bottom = nil,          -- unused
    Obstruction_right_top = {22, 23, 24},   -- RGB
    Obstruction_right_bottom = nil          -- unused
}


function SetLightsStatus(name, color_or_boolean) -- set the status of a light (in LIGHTS_STATUS and on the screen)
    LIGHTS_STATUS[name] = color_or_boolean
    if LIGHTS_CHANNELS[name] == nil then
        return
    elseif LIGHT_TYPES[name] == TYPES.RGB then
        for i, channel in ipairs(LIGHTS_CHANNELS[name]) do
            output.setNumber(channel, color_or_boolean[i])
        end
    elseif LIGHT_TYPES[name] == TYPES.STANDARD then
        output.setBool(LIGHTS_CHANNELS[name], color_or_boolean)
    end
end



function drawDraftLights()
    SetLightsStatus("middle_mast_3", COLORS.RED)
    SetLightsStatus("middle_mast_2", COLORS.RED)
    SetLightsStatus("middle_mast_1", COLORS.RED)
end
function drawManeuverLights()
    SetLightsStatus("middle_mast_3", COLORS.RED)
    SetLightsStatus("middle_mast_2", COLORS.WHITE)
    SetLightsStatus("middle_mast_1", COLORS.RED)
end
function drawNoControlLights()
    SetLightsStatus("middle_mast_3", COLORS.RED)
    SetLightsStatus("middle_mast_2", COLORS.RED)
end
function drawMineClearanceLights()
    SetLightsStatus("minesweeper_light", true)
    SetLightsStatus("minesweeper_left_light", true)
    SetLightsStatus("minesweeper_right_light", true)
end

function drawInMovementLights()
    SetLightsStatus("front_mast_3", COLORS.WHITE)
    SetLightsStatus("left_light", true)
    SetLightsStatus("right_light", true)
    SetLightsStatus("rear_light_bottom", true)
end
function drawAnchoredLights()
    SetLightsStatus("front_mast_3", COLORS.WHITE)
end
function drawTowedLights()
    SetLightsStatus("left_light", true)
    SetLightsStatus("right_light", true)
    SetLightsStatus("rear_light_bottom", true)
end

function drawIsPilotLights()
    SetLightsStatus("front_mast_3", COLORS.WHITE)
    SetLightsStatus("front_mast_2", COLORS.RED)
end
function drawTowingAbove200mLights()
    SetLightsStatus("front_mast_3", COLORS.WHITE)
    SetLightsStatus("front_mast_2", COLORS.WHITE)
    SetLightsStatus("front_mast_1", COLORS.WHITE)
    SetLightsStatus("rear_light_top", true)
end
function drawTowingBelow200mLights()
    SetLightsStatus("front_mast_3", COLORS.WHITE)
    SetLightsStatus("front_mast_2", COLORS.WHITE)
    SetLightsStatus("rear_light_top", true)
end
function drawTowingAlongsideLights()
    SetLightsStatus("front_mast_3", COLORS.WHITE)
    SetLightsStatus("front_mast_2", COLORS.WHITE)
    SetLightsStatus("front_mast_1", COLORS.WHITE)
end

function drawObstructionOnLeftLights()
    SetLightsStatus("Obstruction_left_top", COLORS.RED)
    SetLightsStatus("Obstruction_left_bottom", COLORS.RED)
    SetLightsStatus("Obstruction_right_top", COLORS.GREEN)
    SetLightsStatus("Obstruction_right_bottom", COLORS.GREEN)
end
function drawObstructionOnRightLights()
    SetLightsStatus("Obstruction_left_top", COLORS.GREEN)
    SetLightsStatus("Obstruction_left_bottom", COLORS.GREEN)
    SetLightsStatus("Obstruction_right_top", COLORS.RED)
    SetLightsStatus("Obstruction_right_bottom", COLORS.RED)
end


LIGHTS_FUNCTIONS = {
    Restricted_by_draft = drawDraftLights,
    Restricted_maneuverability = drawManeuverLights,
    No_control = drawNoControlLights,
    Mine_clearance = drawMineClearanceLights,
    In_movement = drawInMovementLights,
    Anchored = drawAnchoredLights,
    Towed = drawTowedLights,
    Is_pilot = drawIsPilotLights,
    Towing_above_200m = drawTowingAbove200mLights,
    Towing_below_200m = drawTowingBelow200mLights,
    Towing_alongside = drawTowingAlongsideLights,
    Obstruction_on_left = drawObstructionOnLeftLights,
    Obstruction_on_right = drawObstructionOnRightLights
}


function reset_status()
    for key, value in pairs(LIGHTS_STATUS) do
        if LIGHT_TYPES[key] == TYPES.RGB then
            SetLightsStatus(key, COLORS.OFF)
        elseif LIGHT_TYPES[key] == TYPES.STANDARD then
            SetLightsStatus(key, false)
        end
    end
end

function onTick()
    reset_status()
    for key, value in pairs(INPUTS) do
        if input.getBool(value) then
            LIGHTS_FUNCTIONS[key]()
        end
    end
end



LIGHTS_DATA = {
    SIDE_VIEW_LEFT = {
        front_mast_3 = {x=39, y=9},
        front_mast_2 = {x=37, y=13},
        front_mast_1 = {x=35, y=17},

        middle_mast_3 = {x=50, y=8},
        middle_mast_2 = {x=50, y=12},
        middle_mast_1 = {x=50, y=15},

        rear_light_top = {x=135, y=50}, -- yellow towing light
        rear_light_bottom = {x=135, y=55},

        left_light = {x=35, y=30},
        right_light = nil,

        minesweeper_left_light = {x=65, y=15},
        minesweeper_right_light = nil,
        minesweeper_light = {x=65, y=8},

        Obstruction_left_top = {x=100, y=22},
        Obstruction_left_bottom = {x=100, y=25},
        
        Obstruction_right_top = nil,
        Obstruction_right_bottom = nil,

    },
    SIDE_VIEW_RIGHT = {
        front_mast_3 = {x=105, y=9},
        front_mast_2 = {x=107, y=13},
        front_mast_1 = {x=109, y=17},

        middle_mast_3 = {x=94, y=8},
        middle_mast_2 = {x=94, y=12},
        middle_mast_1 = {x=94, y=15},

        rear_light_top = {x=9, y=50}, -- yellow towing light
        rear_light_bottom = {x=9, y=55},

        left_light = nil,
        right_light = {x=109, y=30},

        minesweeper_left_light = nil,
        minesweeper_right_light = {x=79, y=15},
        minesweeper_light = {x=79, y=8},

        Obstruction_left_top = nil,
        Obstruction_left_bottom = nil,
        
        Obstruction_right_top = {x=44, y=22},
        Obstruction_right_bottom = {x=44, y=25},
    },
    TOP_VIEW = {
        front_mast_3 = {x=72, y=50},
        front_mast_2 = {x=72, y=52},
        front_mast_1 = {x=72, y=54},

        middle_mast_3 = {x=72, y=60},
        middle_mast_2 = {x=72, y=62},
        middle_mast_1 = {x=72, y=64},

        left_light = {x=39, y=59},
        right_light = {x=105, y=59},

        rear_light_top = {x=72, y=155}, -- yellow towing light
        rear_light_bottom = {x=72, y=155},

        minesweeper_left_light = {x=56, y=77},
        minesweeper_right_light =  {x=88, y=77},
        minesweeper_light =  {x=72, y=77},

        Obstruction_left_top = {x=48, y=129},
        Obstruction_left_bottom = nil,
        
        Obstruction_right_top = {x=96, y=129},
        Obstruction_right_bottom = nil,
    }
}


POSITIONS = {
    SIDE_VIEW_LEFT = {x=0, y=0},
    SIDE_VIEW_RIGHT = {x=0, y=80},
    TOP_VIEW = {x=144, y=0}
}



function SetLights(name, color)
    if color == COLORS.OFF then
        return
    end
    for viewName, data in pairs(LIGHTS_DATA) do
        if data[name] then
            screen.setColor(color[1], color[2], color[3])
            local x = data[name].x + POSITIONS[viewName].x
            local y = data[name].y + POSITIONS[viewName].y
            screen.drawRectF(x-1,y,3,1)
            screen.drawRectF(x,y-1,1,3)
        end
    end
end


function onDraw()
    for key, value in pairs(LIGHTS_STATUS) do
        if LIGHT_TYPES[key] == TYPES.RGB then
            SetLights(key, value)
        elseif LIGHT_TYPES[key] == TYPES.STANDARD then
            if value then
                SetLights(key, LIGHTS_COLORS[key])
            end
        end
    end
end