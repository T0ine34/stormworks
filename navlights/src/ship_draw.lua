
-- available dimensions = 144x80
SIDE_VIEW_LEFT = {
    { -- hull
        {x=5,   y=40 },
        {x=20,  y=75 },
        {x=120, y=75 },
        {x=134, y=61 },
        {x=134, y=50 },
        {x=95,  y=50 },
        {x=85,  y=40 },
        {x=5,   y=40 }
    },
    { -- bridge
        {x=25,  y=40 },
        {x=32,  y=28 },
        {x=24,  y=20 },
        {x=65,  y=20 },
        {x=65,  y=30 },
        {x=70,  y=30 },
        {x=70,  y=40 }
    },
    { -- crane
        {x=75,  y=40 },
        {x=75,  y=30 },
        {x=100,  y=25 },
        {x=100,  y=27 },
        {x=80,  y=32 },
        {x=80,  y=40 }
    },
    { -- front mast
        {x=30,  y=20 },
        {x=40,  y=5  },
        {x=43,  y=5  },
        {x=38,  y=20 }
    },
    { -- middle mast
        {x=50,  y=20 },
        {x=50,  y=8  }
    }
}

-- available dimensions = 144x80
SIDE_VIEW_RIGHT = {
    { -- hull
        {x=139, y=40 },
        {x=124, y=75 },
        {x=24,  y=75 },
        {x=10,  y=61 },
        {x=10,  y=50 },
        {x=49,  y=50 },
        {x=59,  y=40 },
        {x=139, y=40 }
    },
    { -- bridge
        {x=119, y=40 },
        {x=112, y=28 },
        {x=120, y=20 },
        {x=79,  y=20 },
        {x=79,  y=30 },
        {x=74,  y=30 },
        {x=74,  y=40 }
    },
    { -- crane
        {x=69,  y=40 },
        {x=69,  y=30 },
        {x=44,  y=25 },
        {x=44,  y=27 },
        {x=64,  y=32 },
        {x=64,  y=40 }
    },
    { -- front mast
        {x=114, y=20 },
        {x=104, y=5  },
        {x=101, y=5  },
        {x=106, y=20 }
    },
    { -- middle mast
        {x=94,  y=20 },
        {x=94,  y=8  }
    }
}

-- available dimensions = 144x160
TOP_VIEW = {
    { -- front hull
        {x=97, y=55},
        {x=72, y=5},
        {x=47, y=55}
    },
    { -- rear hull
        {x= 44, y=65},
        {x= 44, y=155},
        {x=100, y=155},
        {x=100, y=65}
    },
    { -- container bay left
        {x=55, y=80},
        {x=55, y=110},
        {x=68, y=110},
        {x=68, y=80},
    },
    { -- container bay right
        {x=76, y=80},
        {x=76, y=110},
        {x=89, y=110},
        {x=89, y=80},
    },
    { -- bridge
        {x=60, y=45},
        {x=55, y=50},
        {x=55, y=55},
        {x=40, y=55},
        {x=40, y=65},
        {x=55, y=65},
        {x=55, y=80},
        {x=89, y=80},
        {x=89, y=65},
        {x=104, y=65},
        {x=104, y=55},
        {x=89, y=55},

        {x=89, y=50},
        {x=84, y=45},
        {x=60, y=45}
    },
    { -- crane left base
        {x=46, y=105},
        {x=46, y=110},
        {x=51, y=110},
        {x=51, y=105},
        {x=46, y=105}
    },
    {
        -- crane left arm
        {x=46, y=110},
        {x=48, y=130},
        {x=49, y=130},
        {x=51, y=110}
    },
    { -- crane right base
        {x=93, y=105},
        {x=93, y=110},
        {x=98, y=110},
        {x=98, y=105},
        {x=93, y=105}
    },
    {
        -- crane right arm
        {x=93, y=110},
        {x=95, y=130},
        {x=96, y=130},
        {x=98, y=110}
    }
}

POSITIONS = {
    SIDE_VIEW_LEFT = {x=0, y=0},
    SIDE_VIEW_RIGHT = {x=0, y=80},
    TOP_VIEW = {x=144, y=0}
}


function DrawItem(x, y, item)
    screen.setColor(32,32,32)
    for _, subitem in ipairs(item) do
        for i = 1, #subitem-1 do
            screen.drawLine(x + subitem[i].x, y + subitem[i].y, x + subitem[i+1].x, y + subitem[i+1].y)
        end
    end
end

function DrawHelipad(x, y)
    screen.setColor(32, 32, 32)
    screen.drawCircle(x, y+1, 15)
    screen.drawRectF(x - 8, y - 8, 3, 17)
    screen.drawRectF(x + 5, y - 8, 3, 17)
    screen.drawRectF(x - 5, y - 1, 10, 3)

end

function onDraw()
    screen.setColor(64, 64, 64)
    screen.drawLine(144, 0, 144, 160)
    screen.drawLine(0, 80, 144, 80)

    DrawItem(POSITIONS.SIDE_VIEW_LEFT.x,  POSITIONS.SIDE_VIEW_LEFT.y,  SIDE_VIEW_LEFT)
    DrawItem(POSITIONS.SIDE_VIEW_RIGHT.x, POSITIONS.SIDE_VIEW_RIGHT.y, SIDE_VIEW_RIGHT)
    DrawItem(POSITIONS.TOP_VIEW.x,        POSITIONS.TOP_VIEW.y,        TOP_VIEW)

    DrawHelipad(POSITIONS.TOP_VIEW.x + 72, POSITIONS.TOP_VIEW.y + 135)
end