import shutil
import subprocess
import toml


def update_version(
        version: str,
        update_type='patch'
) -> str:
    """
    주어진 버전 문자열을 업데이트합니다.

    :param version: 업데이트할 버전 문자열 (예: '0.0.0')
    :param update_type: 업데이트할 유형 ('major', 'minor', 'patch' 중 하나)
    :return: 업데이트된 버전 문자열
    """
    # 버전 문자열을 숫자 리스트로 분해
    major, minor, patch = map(int, version.split('.'))

    # 업데이트 유형에 따른 버전 증가
    if update_type == 'major':
        major += 1
        minor, patch = 0, 0  # major 업데이트 시 나머지 초기화
    elif update_type == 'minor':
        minor += 1
        patch = 0  # minor 업데이트 시 patch 초기화
    elif update_type == 'patch':
        patch += 1

    return f"{major}.{minor}.{patch}"


def update_package_version(update_type='patch'):
    pyproject_path = 'pyproject.toml'

    with open(pyproject_path, 'r', encoding='utf-8') as f:
        data = toml.load(f)

    version = update_version(data['project']['version'], update_type)

    data['project']['version'] = version

    with open(pyproject_path, 'w', encoding='utf-8') as f:
        toml.dump(data, f)


def clean_dist():
    """dist 디렉토리를 삭제합니다."""
    shutil.rmtree('dist', ignore_errors=True)


def build_package():
    """패키지를 빌드합니다."""
    result = subprocess.run(['python', '-m', 'build'], encoding='utf-8')
    return result.returncode == 0  # 빌드 성공 여부 반환


def upload_package():
    """빌드된 패키지를 PyPI에 업로드합니다."""
    try:
        # twine 명령 실행, stderr를 파이프에 연결하여 오류 메시지 캡처
        result = subprocess.run(['twine', 'upload', 'dist/*'], check=True, capture_output=True, text=True, encoding='utf-8')
        print("패키지가 성공적으로 PyPI에 업로드되었습니다.")
    except subprocess.CalledProcessError as e:
        # 오류 메시지가 'File already exists'를 포함하는지 확인
        if "File already exists" in e.stderr:
            print("버전이 같아서 PyPI에 배포할 수 없습니다. 패키지 버전을 업데이트한 후 다시 시도하세요.")
        else:
            # 다른 종류의 오류일 경우 기본 오류 메시지 출력
            print("패키지 업로드 중 오류가 발생했습니다:", e.stderr)


def upload_to_github():
    """변경 사항을 GitHub에 커밋하고 푸시합니다."""
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', 'Build and upload package'])
    subprocess.run(['git', 'push', 'origin', 'emotions'])  # 'emotions'을 사용 중인 브랜치 이름으로 변경
