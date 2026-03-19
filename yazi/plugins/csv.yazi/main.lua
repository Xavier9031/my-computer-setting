--- @since 26.1.22

local M = {}

local function fail(job, s)
	ya.preview_widget(job, ui.Text.parse(s):area(job.area):wrap(ui.Wrap.YES))
end

function M:peek(job)
	local child, err = Command("sh")
		:arg({ "-c", 'python3 ~/.config/yazi/scripts/csv_preview.py "$1" "$h"', "sh", tostring(job.file.path) })
		:env("h", tostring(job.area.h))
		:stdout(Command.PIPED)
		:stderr(Command.PIPED)
		:spawn()

	if not child then
		return fail(job, "spawn failed: " .. tostring(err))
	end

	local limit = job.area.h
	local i, outs, errs = 0, {}, {}
	repeat
		local line, event = child:read_line()
		if event == 1 then
			errs[#errs + 1] = line
		elseif event ~= 0 then
			break
		end
		i = i + 1
		if i > job.skip then
			outs[#outs + 1] = line
		end
	until i >= job.skip + limit

	child:start_kill()

	if #errs > 0 then
		fail(job, table.concat(errs, ""))
	elseif job.skip > 0 and i < job.skip + limit then
		ya.emit("peek", { math.max(0, i - limit), only_if = job.file.url, upper_bound = true })
	else
		ya.preview_widget(job, ui.Text.parse(table.concat(outs, "")):area(job.area))
	end
end

function M:seek(job) require("code"):seek(job) end

return M
