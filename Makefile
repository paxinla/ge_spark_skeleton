UTILSH = "mkutils/util.sh"
VMROOT := ENV
PYCMD := $(VMROOT)/bin/python
PIPCMD := $(VMROOT)/bin/pip


init:
	@[ -d "$(VMROOT)" ] || { echo "You need to make a virtual environment named $(VMROOT) first!"; exit 1; }
	@$(UTILSH) gen_root
	@$(UTILSH) gen_setup_py
	@test -d $(VMROOT) && $(PIPCMD) install -r requirements.txt
	@$(UTILSH) gen_bone_files


wheel:
	@$(UTILSH) gen_manifest
	@test -f *.whl && rm *.whl || true
	$(PYCMD) setup.py sdist bdist_wheel
	@mv dist/*.whl ./
	@test -d build && rm -r build || true
	@test -d dist && rm -r dist || true
	@test -d *.egg-info && rm -r *.egg-info || true

