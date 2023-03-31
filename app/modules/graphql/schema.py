type_defs = """
    scalar Datetime
    scalar Date

    type Query {
        tags(tagId: Int): [Tag]!
        getCategories(catId: Int): CategoriesResult!
        getRooms(roomId: Int): RoomsResult!
        photos(photoId: Int): [Photo]!
        clients(clientId: Int): [Client]!
        orders(orderId: Int): [Order]!
        purchases(purchaseId: Int): [Purchase]!
        sales(saleId: Int): [Sale]!
    }
    
    type RoomsResult {
        status: MutationStatus!
        rooms: [Room]
    }
    
     type CategoriesResult {
        status: MutationStatus!
        categories: [Category]
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
        
        createSale(
            input: CreateSaleInput!
        ): SaleResult!
        
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
        
        updateSale(
            id: Int!
            input: UpdateSaleInput!
        ): SaleResult!
        
        deleteRoom(
            id: Int!
        ): DeleteResult!
        
        deletePhoto(
            id: Int!
        ): DeleteResult!
        
        deleteSale(
            id: Int!
        ): DeleteResult!
        
        deleteCategory(
            id: Int!
        ): DeleteResult!
        
        deleteTag(
            id: Int!
        ): DeleteResult!
        
        cancelPurchase(
            id: Int!
        ): PurchaseResult!
        
        cancelOrder(
            id: Int!
        ): OrderResult!
        
        addTagToCategory(
            tagId: Int!
            categoryId: Int!
        ): TagCategoryResult!
        
        addSaleToCategory(
            saleId: Int!
            categoryId: Int!
        ): SaleCategoryResult!
        
        removeTagFromCategory(
            tagId: Int!
            categoryId: Int!
        ): TagCategoryResult!
        
        removeSaleFromCategory(
            saleId: Int!
            categoryId: Int!
        ): SaleCategoryResult!
        
        login(
            login: String!
            password: String!
        ): LoginResult!
        
        singUp(
            input: SingUpInput!
        ): ClientResult!
        
        refreshToken(
            refreshToken: String!
        ): LoginResult!
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
    
    input CreateSaleInput {
        name: String!
        description: String!
        discount: Float!
        image_path: String!
        startDate: Datetime!
        endDate: Datetime!
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
    
    input UpdateSaleInput {
        name: String
        description: String
        discount: Float
        image_path: String
        startDate: Datetime
        endDate: Datetime
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
    
    input SingUpInput {
        email: String!
        password: String!
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
    
    type LoginResult {
        status: MutationStatus!
        tokens: AuthTokens
    }
    
    type SaleResult {
        status: MutationStatus!
        sale: Sale
    }
    
    type TagCategoryResult {
        status: MutationStatus!
        tag: Tag
        category: Category
    }
    
    type SaleCategoryResult {
        status: MutationStatus!
        sale: Sale
        category: Category
    }
    
    type DeleteResult {
        status: MutationStatus!
    }
    
    type MutationStatus {
        success: Boolean!
        error: String
    }
    
    type Room {
        id: Int!
        roomNumber: Int!
        category: Category!
    }
    
    type Photo {
        id: Int!
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
        getRooms: RoomsResult
        familiar: [Category]!
        sales: [Sale]!
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
        refund: Float
        isPaid: Boolean!
        isPrepaymentPaid: Boolean!
        isCanceled: Boolean!
        order: Order!
        room: Room!
    }
    
    type Sale {
        id: Int!
        name: String!
        description: String!
        discount: Float!
        image_path: String!
        startDate: Datetime!
        endDate: Datetime!
        categories: [Category]!
    }
    
    type AuthTokens {
        access_token: String!
        refresh_token: String!
    }
"""
