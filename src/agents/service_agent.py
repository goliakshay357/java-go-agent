class ServiceAgent:
    def __init__(self):
        pass

    def prompt(self, service_code: str):
        return f"""
            Role: You are an expert software engineer converting Java Play Framework code to Golang.
            Goal: Convert the following Java class to Golang: (It's a service code)

            Instructions:
                - **Strictly follow the Java class structure.**
                - Use **GORM v2 for ORM**, but do not add database initialization.
                - For Database, detect the right database and use the right ORM. 
                - If you detect read vs write on the DB operations, then build that capability in the code.
                - Use **Zap for logging**, but do not add extra logging functions unless they exist in Java.
                - Use **Sarama for Kafka**.
                - Use **https://github.com/redis/go-redis** for Redis.
                - Convert **Java/ Play Frameworks's micrometer metrics to Prometheus. Convert JVM metrics to meaningful metrics or ignore if not found**
                - Use **godotenv** and `.env` for configurations but do not add setup code.
                - **Do not add extra frameworks** like Gin, Kafka, or CLI tools.
                - **Ensure JSON responses and error codes are identical to the Java application.**
                - **Do not add main() or extra methods unless they exist in Java.**
                - ** If you detect java / play framework specific threading, move them into go routines with a comment on the code as `uses go routines`**

            Here is the service code:
            {service_code}

            Other Instructions:
            - Retain **method and class names**.
            - Do **not** modify method signatures.
            - Do **not** introduce new features.
            - Do **not** change the folder structure.
            - Use the right golang package name/format - for instance `package api.utils.domain` should be `domain` in case the file being saved is in `domain` folder.
            - Use **`github.com/ne-bank-cbs/cbs-utils/`** as the package prefix for imports.
            - If you detect an ORM model, only then use GORM models. Else use the standard structs.
            - Ensure **clean, simple, well-documented Go code**.
            - give file name and a comment of original file name in the code
            - Very important: DOnt add anything extra or your overthinking and add some extra code. dont act smart. just convert the necessary code. Just convert the given code.
            - As you are deadling with service code, you need to be carefully on redis utils and other important utils. Never miss anything on it's data type and all. 

            Few Important Notes:
            - If anything in doubt or not provided, feel free to ask before generating the code. 
            - If any variable is not provided, please ask, like one case is we have inmemory caches in java code, that's why. 
            - Tomorrow I might go to postgres but currently is ms sql. so keep orm funtions keep it carefully
            - Calling any external functions like from utils, auth? Mention them in a section called checklist. 
                Sample: 
                    [ ] dataframe.utils() is been called. 

            Sample example: ** Only for you to understand the code structing and linking between the files, what files to create and nothing else, ofcourse nothing concrete but you can do whatever is good as per industry standards **

            ```go
            // file: tags_service.go:
            package service
            import (
                "golang-crud-gin/data/request"
                "golang-crud-gin/data/response"
            )

            type TagsService interface {{
                Create(tags request.CreateTagsRequest)
                Update(tags request.UpdateTagsRequest)
                Delete(tagsId int)
                FindById(tagsId int) response.TagsResponse
                FindAll() []response.TagsResponse
            }}

            // file: tags_service_impl.go:
            package service

            import (
                "golang-crud-gin/data/request"
                "golang-crud-gin/data/response"
                "golang-crud-gin/helper"
                "golang-crud-gin/model"
                "golang-crud-gin/repository"

                "github.com/go-playground/validator/v10"
            )

            type TagsServiceImpl struct {{
                TagsRepository repository.TagsRepository
                Validate       *validator.Validate
            }}

            func NewTagsServiceImpl(tagRepository repository.TagsRepository, validate *validator.Validate) TagsService {{
                return &TagsServiceImpl{{
                    TagsRepository: tagRepository,
                    Validate:       validate,
                }}
            }}

            // Create implements TagsService
            func (t *TagsServiceImpl) Create(tags request.CreateTagsRequest) {{
                err := t.Validate.Struct(tags)
                helper.ErrorPanic(err)
                tagModel := model.Tags{{
                    Name: tags.Name,
                }}
                t.TagsRepository.Save(tagModel)
            }}

            // Delete implements TagsService
            func (t *TagsServiceImpl) Delete(tagsId int) {{
                t.TagsRepository.Delete(tagsId)
            }}

            // Update implements TagsService
            func (t *TagsServiceImpl) Update(tags request.UpdateTagsRequest) {{
                tagData, err := t.TagsRepository.FindById(tags.Id)
                helper.ErrorPanic(err)
                tagData.Name = tags.Name
                t.TagsRepository.Update(tagData)
            }}
            ```
        """