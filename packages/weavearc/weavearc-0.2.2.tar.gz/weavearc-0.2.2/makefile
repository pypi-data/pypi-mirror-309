typecheck:
	uvx mypy --python-executable "./.venv/bin/python3.10" .
	uvx pyright --pythonpath "./.venv/bin/python3.10"

push-release:
	git add .
	git commit -m "Release"
	git push origin master
	gh release list