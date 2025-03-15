class ControllerAgent:
    def __init__(self):
        pass

    def prompt(self, controller_code: str):
        return f"""
            Role: You are an expert software engineer converting Java Play Framework code to Golang.
            Goal: Convert the following Java class to Golang: (It's a controller code)

            Instructions:
                - Use **GORM v2 for ORM**, but do not add database initialization.
                - Use **Zap for logging**, but do not add extra logging functions unless they exist in Java.
                - Use **Sarama for Kafka**.
                - Use **https://github.com/redis/go-redis** for Redis.
                - Convert **Java/ Play Frameworks's micrometer metrics to Prometheus. Convert JVM metrics to meaningful metrics or ignore if not found**
                - Use **godotenv** and `.env` for configurations but do not add setup code.
                - **Do not add extra frameworks** like Gin, Kafka, or CLI tools.
                - **Ensure JSON responses and error codes are identical to the Java application.**
                - **Do not add main() or extra methods unless they exist in Java.**
                - ** If you detect java / play framework specific threading, move them into go routines with a comment on the code as `uses go routines`**


            Here is the controller code:
            {controller_code}


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
            - As you are deadling with controller code, you need to be carefully on request and response handling. Never miss anything on it's data type and all. 

            
            Few Important Notes:
            - If anything in doubt or not provided, feel free to ask before generating the code. 
            - Tomorrow I might go to postgres but currently is ms sql. so keep orm funtions keep it carefully
            - Calling any external functions like from utils, auth? Mention them in a section called checklist. 
                Sample: 
                    [ ] dataframe.utils() is been called. 
            
            
            Sample example: ** Only for you to understand the code structing and linking between the files, what files to create and nothing else, ofcuour nothing concrete but you can do whatever is good as per industry standards **
            
            ```go
            // file: router.go:
            func NewRouter(tagsController *controller.TagsController) *gin.Engine {{
                router := gin.Default()
                // add swagger
                router.GET("/docs/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

                router.GET("", func(ctx *gin.Context) {{
                    ctx.JSON(http.StatusOK, "welcome home")
                }})
                baseRouter := router.Group("/api")
                tagsRouter := baseRouter.Group("/tags")
                tagsRouter.GET("", tagsController.FindAll)
                tagsRouter.GET("/:tagId", tagsController.FindById)
                tagsRouter.POST("", tagsController.Create)
                tagsRouter.PATCH("/:tagId", tagsController.Update)
                tagsRouter.DELETE("/:tagId", tagsController.Delete)

                return router
            }}

            // file: tags_controller.go:
            type TagsController struct {{
                tagsService service.TagsService
            }}

            func NewTagsController(service service.TagsService) *TagsController {{
                return &TagsController{{
                    tagsService: service,
                }}
            }}

            func (controller *TagsController) Create(ctx *gin.Context) {{
                log.Info().Msg("create tags")
                createTagsRequest := request.CreateTagsRequest{{}}
                err := ctx.ShouldBindJSON(&createTagsRequest)
                helper.ErrorPanic(err)

                controller.tagsService.Create(createTagsRequest)
                webResponse := response.Response{{
                    Code:   http.StatusOK,
                    Status: "Ok",
                    Data:   nil,
                }}
                ctx.Header("Content-Type", "application/json")
                ctx.JSON(http.StatusOK, webResponse)
            }}

            // data/request.go: (For all DTOs in /data folder)
            package request

            type CreateTagsRequest struct {{
                Name string `validate:"required,min=1,max=200" json:"name"`
            }}

            // data/response.go: (For all DTOs in /data folder)
            package response

            type TagsResponse struct {{
                Id   int    `json:"id"`
                Name string `json:"name"`
            }}
            ```
        """