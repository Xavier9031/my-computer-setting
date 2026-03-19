local M = {}

function M:peek(job)
	ya.preview_widget(job, ui.Text("CSV PLUGIN LOADED"):area(job.area))
end

function M:seek(job) end

return M
