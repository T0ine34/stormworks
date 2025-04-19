-- made by Antoine Buirey

ROTATING_COMPASS_CHANNEL = 7
DISTANCE_SENSOR_CHANNEL = 8
SHIP_ROTATION_CHANNEL = 9
RANGE_CHANNEL = 10

DETECTED_OBJECTS = {}


PI2 = math.pi*2

TIMER = 0

function onTick()
    rads_from_east = math.fmod((-input.getNumber(ROTATING_COMPASS_CHANNEL)+1.75)*PI2, PI2)

    ship_rad_from_east = math.fmod((input.getNumber(SHIP_ROTATION_CHANNEL)+1.25)*PI2, PI2)

    rads_from_right = math.fmod(rads_from_east - ship_rad_from_east + PI2, PI2) -- angle from the right of the ship

    distance = input.getNumber(DISTANCE_SENSOR_CHANNEL)
    max_distance = input.getNumber(RANGE_CHANNEL)

    obj_life = property.getNumber("Object life")

    -- remove old objects
    for i, object in ipairs(DETECTED_OBJECTS) do
        if object.timer + obj_life < TIMER then
            table.remove(DETECTED_OBJECTS, i)
        end
    end


    -- coordinates in a cartesian plane of size max_distance x max_distance

    if distance < max_distance then
        table.insert(DETECTED_OBJECTS, {distance=distance, angle=rads_from_right, timer=TIMER})
    end

    TIMER = TIMER + 1
end



function drawShipIcon(x, y)
    -- a small ship icon facing top
    -- x, y is the center of the ship
    screen.setColor(127, 127, 127)
    screen.drawLine(x, y-5, x+2, y-1)
    screen.drawLine(x, y-5, x-2, y-1)
    screen.drawLine(x+2, y-1, x+2, y+5)
    screen.drawLine(x-2, y-1, x-2, y+5)
    screen.drawLine(x+2, y+5, x-2, y+5)
end



function onDraw()
    local width = screen.getWidth()
    local height = screen.getHeight()

    local radar_width = width - 20
    local radar_height = height - 20

    local size = math.min(width, height)

    local cardinal_size = size - 10
    local radar_size = math.min(radar_width, radar_height)
    screen.setColor(0, 127, 0)

    screen.drawCircle(width/2, height/2, radar_size/2) -- outer circle
    screen.drawCircle(width/2, height/2, radar_size/4) -- inner circle


    -- cardinal points using ship rotation
    screen.setColor(127, 127, 127)
    screen.drawText(width/2 + cardinal_size/2 * math.cos(ship_rad_from_east) - 2,
                    height/2 + cardinal_size/2 * math.sin(ship_rad_from_east) - 2, "S")
    screen.drawText(width/2 + cardinal_size/2 * math.cos(math.fmod(ship_rad_from_east + math.pi/2, PI2)) - 2,
                    height/2 + cardinal_size/2 * math.sin(math.fmod(ship_rad_from_east + math.pi/2, PI2)) - 2, "W")
    screen.drawText(width/2 + cardinal_size/2 * math.cos(math.fmod(ship_rad_from_east + math.pi, PI2)) - 2,
                    height/2 + cardinal_size/2 * math.sin(math.fmod(ship_rad_from_east + math.pi, PI2)) - 2, "N")
    screen.drawText(width/2 + cardinal_size/2 * math.cos(math.fmod(ship_rad_from_east + 3*math.pi/2, PI2)) - 2,
                    height/2 + cardinal_size/2 * math.sin(math.fmod(ship_rad_from_east + 3*math.pi/2, PI2)) - 2, "E")

    drawShipIcon(width/2, height/2)


    screen.drawLine(width/2,
                    height/2,
                    width/2 + radar_size/2 * math.cos(rads_from_right),
                    height/2 + radar_size/2 * math.sin(rads_from_right)
                ) -- compass needle

    for i, object in ipairs(DETECTED_OBJECTS) do
        life_ratio = (object.timer + obj_life - TIMER) / obj_life
        screen.setColor(0, 127, 0, 127 * life_ratio)
        screen.drawRectF(width/2 + object.distance * radar_size/2/max_distance * math.cos(object.angle),
        height/2 + object.distance * radar_size/2/max_distance * math.sin(object.angle),
                        1, 1
                    )
    end
end