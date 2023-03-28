type_defs = """
    scalar Datetime
    scalar Date

    type Query {
        hello: String!
        tags(tagId: Int): [Tag]!
        categories(catId: Int): [Category]!
        rooms(roomId: Int): [Room]!
        photos(photoId: Int): [Photo]!
    }
    
    type Mutation {
        createTag(
            input: CreateTagInput!
        ): TagResult!
        
        createCategory(
            input: CreateCategoryInput!
        ): CategoryResult
        
        createRoom(
            input: CreateRoomInput!
        ): RoomResult!
        
        createPhoto(
            input: CreatePhotoInput!
        ): PhotoResult!
        
        updatePhoto(
            id: Int!
            input: UpdatePhotoInput!
        ): PhotoResult!
        
        updateCategory(
            id: Int!
            input: UpdateCategoryInput!
        ): CategoryResult!
        
        updateRoom(
            id: Int!
            input: UpdateRoomInput!
        ): RoomResult!
        
        updateTag(
            id: Int!
            input: UpdateTagInput!
        ): TagResult!
        
        addTagToCategory(
            tag_id: Int!
            category_id: Int!
        ): TagCategoryResult!
    }
    
    input CreateRoomInput {
        roomNumber: Int
        categoryId: Int!
    }
    
    input CreateCategoryInput {
        name: String!
        description: String!
        price: Float!
        prepayment_percent: Float!
        refund_percent: Float!
        main_photo_path: String!
        rooms_count: Int!
        floors: Int!
        beds: Int!
        square: Float!
    }
    
    input CreatePhotoInput {
        path: String!
        categoryId: Int!
    }
    
    input CreateTagInput {
        name: String!
    }
    
    input UpdatePhotoInput {
        path: String
        order: Int
    }
    
    input UpdateRoomInput {
        roomNumber: Int
    }
    
    input UpdateCategoryInput {
        name: String
        description: String
        price: Float
        prepayment_percent: Float
        refund_percent: Float
        main_photo_path: String
        rooms_count: Int
        floors: Int
        beds: Int
        square: Float
    }
    
    input UpdateTagInput {
        name: String
    }
    
    type RoomResult {
        status: MutationStatus!
        room: Room
    }
    
    type CategoryResult {
        status: MutationStatus!
        category: Category
    }
    
    type PhotoResult {
        status: MutationStatus!
        photo: Photo
    }
    
    type TagResult {
        status: MutationStatus!
        tag: Tag
    }
    
    type TagCategoryResult {
        status: MutationStatus!
        tag: Tag
        category: Category
    }
    
    type MutationStatus {
        success: Boolean!
        error: String
    }
    
    type Room {
        roomNumber: Int!
        category: Category!
    }
    
    type Photo {
        order: Int!
        category: Category!
        path: String!
    }
    
    type Tag {
        id: Int!
        name: String!
        categories: [Category]!
    }
    
    type Category {
        id: Int!
        name: String!
        description: String!
        price: Float!
        prepayment_percent: Float!
        refund_percent: Float!
        main_photo_path: String!
        rooms_count: Int!
        floors: Int!
        beds: Int!
        square: Float!
        tags: [Tag]!
    }
"""
