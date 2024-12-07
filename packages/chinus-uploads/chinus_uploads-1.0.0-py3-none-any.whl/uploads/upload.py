import sys
from typing import Literal
from chinus import has_modified_files
from __uploads import *



def upload(git=True, pypi=True, version: Literal['major', 'minor', 'patch'] = 'patch'):
    # 변경 사항이 존재 and pypi 업로드 Ture인 경우
    if has_modified_files() and pypi:
        update_package_version(version)  # project.toml version 업데이트
        clean_dist()  # dist 디렉토리 삭제

    else:
        print("변경 사항이 존재하지 않습니다.")
        sys.exit(0)

    if build_package():  # 빌드 성공 시 업로드 실행
        upload_package()

    else:
        print("빌드 실패! 업로드를 실행하지 않습니다.")
        sys.exit(0)

    if git:  # 깃허브 업로드
        upload_to_github()


if __name__ == "__main__":
    upload()
