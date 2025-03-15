class RepositoryAgent:
    def __init__(self):
        pass

    def prompt(self, repository_code: str):
        # First part of the prompt
        prompt_part1 = f"""
            Role: You are an expert software engineer converting Java Play Framework code to Golang.
            Goal: Convert the following Java class to Golang: (It's a repository code)

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

            Here is the repository code:
            {repository_code}  

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
            - As you are deadling with repository code, you need to be carefully on redis utils and other important utils. Never miss anything on it's data type and all. 

            Few Important Notes:
            - If anything in doubt or not provided, feel free to ask before generating the code. 
            - If any variable is not provided, please ask, like one case is we have inmemory caches in java code, that's why. 
            - Tomorrow I might go to postgres but currently is ms sql. so keep orm funtions keep it carefully
            - Calling any external functions like from utils, auth? Mention them in a section called checklist. 
                Sample: 
                    [ ] dataframe.utils() is been called. 

            Sample example: ** Only for you to understand the code structing and linking between the files, what files to create and nothing else, ofcourse nothing concrete but you can do whatever is good as per industry standards **
        """

        # Go code example as a separate string (not an f-string)
        go_code_example = """
            ```
            // file: tags_repository.go:
            package repository

            import "golang-crud-gin/model"

            type TagsRepository interface {
                Save(tags model.Tags)
                Update(tags model.Tags)
                Delete(tagsId int)
                FindById(tagsId int) (tags model.Tags, err error)
                FindAll() []model.Tags
            }

            // file: tags_repository_impl.go:
            package repository

            import (
                "errors"
                "golang-crud-gin/helper"
                "golang-crud-gin/model"
                "golang-crud-gin/data/request"
                "gorm.io/gorm"
            )

            type TagsRepositoryImpl struct {
                Db *gorm.DB
            }

            func NewTagsRepository(db *gorm.DB) TagsRepository {
                return &TagsRepositoryImpl{
                    Db: db,
                }
            }

            // Delete implements TagsRepository
            func (t *TagsRepositoryImpl) Delete(tagsId int) {
                var tags model.Tags
                result := t.Db.Where("id = ?", tagsId).Delete(&tags)
                helper.ErrorPanic(result.Error)
            }

            // FindAll implements TagsRepository
            func (t *TagsRepositoryImpl) FindAll() []model.Tags {
                var tags []model.Tags
                result := t.Db.Find(&tags)
                helper.ErrorPanic(result.Error)
                return tags
            }

            // FindById implements TagsRepository
            func (t *TagsRepositoryImpl) FindById(tagsId int) (tags model.Tags, err error) {
                var tag model.Tags
                result := t.Db.Find(&tag, tagsId)
                if result != nil {
                    return tag, nil
                } else {
                    return tag, errors.New("tag is not found")
                }
            }

            // Save implements TagsRepository
            func (t *TagsRepositoryImpl) Save(tags model.Tags) {
                result := t.Db.Create(&tags)
                helper.ErrorPanic(result.Error)
            }

            // Update implements TagsRepository
            func (t *TagsRepositoryImpl) Update(tags model.Tags) {
                var updateTag = request.UpdateTagsRequest{
                    Id:   tags.Id,
                    Name: tags.Name,
                }
                result := t.Db.Model(&tags).Updates(updateTag)
                helper.ErrorPanic(result.Error)
            }

            // Similar for models, DTOs:
            type Tags struct {
                Id   int    `gorm:"type:int;primary_key"`
                Name string `gorm:"type:varchar(255)"`
            }
            ```
        """

        # Combine the parts
        return prompt_part1 + go_code_example
