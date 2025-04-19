PORT = 3000

BOOL_STATES_OUTPUT = { false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false }
NUMBER_STATES_OUTPUT = { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 }

function setOutput()
    for i = 1, 32 do
        output.setBool(i, BOOL_STATES_OUTPUT[i])
        output.setNumber(i, NUMBER_STATES_OUTPUT[i])
    end
end

function buildUrl(layout_name)

    url = "/game/" .. layout_name .. "?"
    for i = 1, 32 do
        url = url .. "b" .. i .. "=" .. tostring(input.getBool(i)) .. "&"
        url = url .. "n" .. i .. "=" .. tostring(input.getNumber(i)) .. "&"
    end
    return url
end

function onTick()
    layout_name = property.getText("Layout name")
    async.httpGet(PORT, buildUrl(layout_name))
    setOutput()
end


function split(inputstr, sep)
    if sep == nil then
        sep = "%."
    end
    local t = {}
    for str in string.gmatch(inputstr, "([^"..sep.."]+)") do
        table.insert(t, str)
    end
    return t
end


function setstates(type, id, value)

    if type == "b" then
        if value == "True" then
            BOOL_STATES_OUTPUT[id] = true
        elseif value == "False" then
            BOOL_STATES_OUTPUT[id] = false
        end
    elseif type == "n" then
        NUMBER_STATES_OUTPUT[id] = tonumber(value)
    end
end

function httpReply(port, url, response_body)
    lines = string.gmatch(response_body, "[^\n]+")
    for line in lines do
        local tokens = split(line, "=")
        local type_id = tokens[1] --
        local value = tokens[2]
        local type_id_tokens = split(type_id, ".")
        local type = type_id_tokens[1] -- b or n
        local id = tonumber(type_id_tokens[2]) -- 1, 2, 3, ...
        if type ~= nil and id ~= nil and value ~= nil then
            setstates(type, id, value)
        end
    end
end
