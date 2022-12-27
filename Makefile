_check_version:
ifndef version
	$(error "version" not defined. example: version=0.18.2)
endif

create-tag: _check_version
	git tag $(version)
	git push origin alpha

delete-tag: _check_version
	-git tag --delete $(version)
	-git push origin --delete $(version)

update-tag: _check_version
	make delete-tag version=$(version)
	make create-tag version=$(version)
