api_key가 하드코딩으로 작성되지 않았는지, 환경변수로 관리하는지 확인 필요. 
이 함수는 에러 발생 시 처리가 불가능하여 try-except 구문 추가 필요.
completion에서 stream=True일 경우, 반응없음 예외처리 필요. 
llama-3.3-70b-specdec 모델에 변경 시 대응할 수 있는 코드 구성 필요. 
completion 생성 시 stop이 None일 경우 멈추지 않는 예외처리 필요.