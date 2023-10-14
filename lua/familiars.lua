local invocable = {}

local DATA_NAMESPACE = 'User'
local DATA_PAGE = 'WikisAreOldschool/data/fams-%s.json'

local FAM_TEMPLATE = [=[|- id="%s"
| rowspan="3" |{{Icon%s}}<br>{{Missing}}
<!--| rowspan="3" |{{Icon%s}}<br>[[File:Familiar_%s.png]]-->
%s
|{{Power}}
|'''%s'''
%s
|-%s
|{{Stamina}}
|'''%s'''
%s
|-
|%s
|{{Agility}}
|'''%s'''
%s
]=] 

local HEADER_TEMPLATE = [[<!-- START AUTO-GENERATED FROM LUA -->
{| class="mw-collapsible bittable grey3" data-expandtext="Show" data-collapsetext="Hide"
|+ %s Familiars
]]
 
local FOOTER_TEMPLATE = [[|}
<!-- END AUTO-GENERATED FROM LUA -->
]]

 
function getJSON(rarity)
    local famTitle = mw.title.makeTitle(DATA_NAMESPACE, string.format(DATA_PAGE, rarity))
    if famTitle and famTitle.exists then
        return famTitle:getContent()
    end

    return ""
end
 
function getFamiliarOutput(fam)
    local name = fam['name']
    local agility = fam['agility']
    local bonuses = fam['bonuses']
    local flavor = fam['flavor']
    local power = fam['power']
    local rarity = fam['rarity']
    local stamina = fam['stamina']
    local dungeons = fam['dungeons']
    local skillDescs = fam['skill_descs']
    local skillNames = fam['skill_names']
    local skillRanges = fam['skill_ranges']
   
    local skillNameCells = {}
    for i, sn in ipairs(skillNames) do
        skillNameCells[i] = string.format("|'''%s'''", sn)
    end

    local skillDescsCells = {}
    for i, sd in ipairs(skillDescs) do
        skillDescsCells[i] = string.format("|%s", sd)
    end

    local skillRangesCells = {}
    for i, sr in ipairs(skillRanges) do
        skillRangesCells[i] = string.format("|%s", sr)
    end

    local nameRowspawn = string.format("|'''%s'''", name)
    local bonusesMarkup = ""
    if #bonuses == 0 then
        nameRowspawn = '| rowspan="2" ' .. nameRowspawn
    else
        bonusesMarkup = string.format("\n|%s\n", table.concat(bonuses, ", "))
    end

    return string.format(
        FAM_TEMPLATE, name, rarity, rarity, name, nameRowspawn, power, table.concat(skillNameCells, "\n"),
        bonusesMarkup, stamina, table.concat(skillDescsCells, "\n"),
        table.concat(dungeons, ", "), agility, table.concat(skillRangesCells, "\n"))
end

function getFamiliarsOutput(rarity, fams)
    local header = string.format(HEADER_TEMPLATE, rarity)

    local fragments = {}
    for i, fam in ipairs(fams) do
        fragments[i] = getFamiliarOutput(fam)
    end

    local rows = table.concat(fragments, "\n")
    return table.concat({header, rows, FOOTER_TEMPLATE}, "\n")
end

function invocable.familiarsTable(frame)
    local rarity = frame.args[1] or frame.args["rarity"]

    if rarity == nil or rarity == "" then
        return "Please provide a rarity to this template"
    end

    local data = getJSON(rarity)
    if data == "" then
        return "Cannot get JSON"
    end

    local fams = mw.text.jsonDecode(data)
    return getFamiliarsOutput(rarity, fams)
end

return invocable