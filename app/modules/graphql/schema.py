type_defs = """
    scalar Datetime
    scalar Date

    type Query {
        hello: String!
        tags(tagId: Int): [Tag]!
        categories(catId: Int): [Category]!
        rooms(roomId: Int): [Room]!
        photos(photoId: Int): [Photo]!
        clients(clientId: Int): [Client]!
        orders(orderId: Int): [Order]!
        purchases(purchaseId: Int): [Purchase]!
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
        
        createClient(
            input: CreateClientInput!
        ): ClientResult!
        
        createOrder(
            input: CreateOrderInput!
        ): OrderResult!
        
        createPurchase(
            input: CreatePurchaseInput!
        ): PurchaseResult!
        
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
        
        updateClient(
            id: Int!
            input: UpdateClientInput!
        ): ClientResult!
        
        updateOrder(
            id: Int!
            input: UpdateOrderInput!
        ): OrderResult!
        
        updatePurchase(
            id: Int!
            input: UpdatePurchaseInput!
        ): PurchaseResult!
        
        cancelPurchase(
            id: Int!
        ): MutationStatus!
        
        addTagToCategory(
            tagId: Int!
            categoryId: Int!
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
        prepaymentPercent: Float!
        refundPercent: Float!
        mainPhotoPath: String!
        roomsCount: Int!
        floors: Int!
        beds: Int!
        square: Float!
    }
    
    input CreatePhotoInput {
        path: String!
        categoryId: Int!
    }
    
    input CreateClientInput {
        firstName: String
        lastName: String
        email: String!
        dateOfBirth: Date
    }
    
    input CreateTagInput {
        name: String!
    }
    
    input CreateOrderInput {
        clientId: Int!
    }
    
    input CreatePurchaseInput {
        start: Date!
        end: Date!
        categoryId: Int!
        orderId: Int!
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
        prepaymentPercent: Float
        refundPercent: Float
        mainPhotoPath: String
        roomsCount: Int
        floors: Int
        beds: Int
        square: Float
    }
    
    input UpdateClientInput {
        firstName: String
        lastName: String
        email: String
        dateOfBirth: Date
    }
    
    input UpdateTagInput {
        name: String
    }
    
    input UpdateOrderInput {
        comment: String
        paid: Float
        refunded: Float
    }
    
    input UpdatePurchaseInput {
        start: Date
        end: Date
    }
    
    type RoomResult {
        status: MutationStatus!
        room: Room
    }
    
    type ClientResult {
        status: MutationStatus!
        client: Client
    }
    
    type OrderResult {
        status: MutationStatus!
        order: Order
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
    
    type PurchaseResult {
        status: MutationStatus!
        purchase: Purchase
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
        prepaymentPercent: Float!
        refundPercent: Float!
        mainPhotoPath: String!
        roomsCount: Int!
        floors: Int!
        beds: Int!
        square: Float!
        tags: [Tag]!
        rooms: [Room]!
    }
    
    type Client {
        id: Int!
        firstName: String
        lastName: String
        email: String!
        dateOfBirth: Date
    }
    
    type Order {
        id: Int!
        dateCreated: Datetime!
        price: Float!
        prepayment: Float!
        comment: String
        paid: Float!
        refunded: Float!
        leftToPay: Float!
        leftToRefund: Float!
        dateFullPrepayment: Datetime
        dateFullPaid: Datetime
        dateFinished: Datetime
        dateCanceled: Datetime
        client: Client!
        purchases: [Purchase]!
    }
    
    type Purchase {
        id: Int!
        start: Date!
        end: Date!
        price: Float!
        prepayment: Float!
        refund: String
        isPaid: Boolean!
        isPrepaymentPaid: Boolean!
        isRefundMade: Boolean!
        isCanceled: Boolean!
        order: Order!
        room: Room!
    }
"""
