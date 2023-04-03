type_defs = """
    scalar Datetime
    scalar Date
    union UserUnion = Client | Worker
    union BaseOrderUnion = Order | Cart

    type Query {
        getTags(tagId: Int): TagsResult!
        getCategories(catId: Int): CategoriesResult!
        getRooms(roomId: Int): RoomsResult!
        getPhotos(photoId: Int): PhotosResult!
        getClients(clientId: Int): ClientsResult!
        getOrders(orderId: Int): OrdersResult!
        getPurchases(purchaseId: Int): PurchasesResult!
        getSales(saleId: Int): SalesResult!
        getWorkers(workerId: Int): WorkersResult!
        getGroups(groupId: Int): GroupsResult!
        getPermissions(permissionId: Int): PermissionsResult!
        getCart(cartUuid: String!): CartResult!
        getClientOrders(orderId: Int): ClientOrdersResult!
    }
    
    type RoomsResult {
        status: MutationStatus!
        rooms: [Room]
    }
    
     type CategoriesResult {
        status: MutationStatus!
        categories: [Category]
    }
    
    type WorkersResult {
        status: MutationStatus!
        workers: [Worker]
    }
    
    type GroupsResult {
        status: MutationStatus!
        groups: [Group]
    }
    
    type PermissionsResult {
        status: MutationStatus!
        permissions: [Permission]
    }
    
    type ClientsResult {
        status: MutationStatus!
        clients: [Client]
    }
    
    type OrdersResult {
        status: MutationStatus!
        orders: [Order]
    }
    
    type PurchasesResult {
        status: MutationStatus!
        purchases: [Purchase]
    }
    
    type PhotosResult {
        status: MutationStatus!
        photos: [Photo]
    }
    
    type ClientOrdersResult {
        status: MutationStatus!
        orders: [ClientOrder]
    }
    
    type SalesResult {
        status: MutationStatus!
        sales: [Sale]
    }
    
    type TagsResult {
        status: MutationStatus!
        tags: [Tag]
    }
    
    type CartResult {
        status: MutationStatus!
        cart: Cart
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
        
        createCart: Cart!
        
        createPurchase(
            input: CreatePurchaseInput!
        ): PurchaseResult!
        
        createCartPurchase(
            cartUuid: String!
            input: CreateCartPurchaseInput!
        ): PurchaseResult!
        
        createSale(
            input: CreateSaleInput!
        ): SaleResult!
        
        createWorker(
            input: CreateWorkerInput!
        ): WorkerResult!
        
        createGroup(
            input: CreateGroupInput!
        ): GroupResult!
        
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
        
        updateWorker(
            id: Int!
            input: UpdateWorkerInput!
        ): WorkerResult!
        
        updateGroup(
            input: UpdateGroupInput!
        ): GroupResult!
        
        updateOrder(
            id: Int!
            input: UpdateOrderInput!
        ): OrderResult!
        
        updatePurchase(
            id: Int!
            input: UpdatePurchaseInput!
        ): PurchaseResult!
        
        updateCartPurchase(
            cartUuid: String!
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
        
        deleteGroup(
            id: Int!
        ): DeleteResult!
        
        cancelPurchase(
            id: Int!
        ): PurchaseResult!
        
        cancelCartPurchase(
            cartUuid: String!
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
        
        addGroupToWorker(
            groupId: Int!
            workerId: Int!
        ): WorkerGroupResult!
        
        addPermissionToGroup(
            groupId: Int!
            permissionId: Int!
        ): GroupPermissionResult!
        
        removeTagFromCategory(
            tagId: Int!
            categoryId: Int!
        ): TagCategoryResult!
        
        removeSaleFromCategory(
            saleId: Int!
            categoryId: Int!
        ): SaleCategoryResult!
        
        removeGroupFromWorker(
            groupId: Int!
            workerId: Int!
        ): WorkerGroupResult!
        
         removePermissionFromGroup(
            groupId: Int!
            permissionId: Int!
        ): GroupPermissionResult!
        
        login(
            login: String!
            password: String!
        ): LoginResult!
        
        singUp(
            input: SingUpInput!
        ): AccountActionResult!
        
        confirmAccount(
            token: String!
        ): UserResult!
        
        requestReset(
            email: String!
        ): AccountActionResult!
        
        confirmReset(
            token: String!
            password: String!
        ): UserResult!
        
        refreshToken(
            refreshToken: String!
        ): LoginResult!
        
        confirmCart(
            cartUuid: String!
            email: String!
            isFullyPaid: Boolean!
        ): ClientOrderResult!
        
        payClientOrder(
            id: Int!
        ): ClientOrderResult!
        
        cancelClientOrder(
            id: Int!
        ): ClientOrderResult!
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
    
    input CreateWorkerInput {
        firstName: String
        lastName: String
        email: String!
        salary: Float!
    }
    
    input CreateGroupInput {
        name: String!
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
    
    input CreateCartPurchaseInput {
        start: Date!
        end: Date!
        categoryId: Int!
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
    
    input UpdateWorkerInput {
        firstName: String
        lastName: String
        email: String
        salary: Float
    }
    
    input UpdateGroupInput {
        name: String
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
    
    type WorkerResult {
        status: MutationStatus!
        worker: Worker
    }
    
    type GroupResult {
        status: MutationStatus!
        group: Group
    }
    
    type OrderResult {
        status: MutationStatus!
        order: Order
    }
    
    type ClientOrderResult {
        status: MutationStatus!
        order: ClientOrder
    }
    
    type CategoryResult {
        status: MutationStatus!
        category: Category
    }
    
    type UsersResult {
        status: MutationStatus!
        users: [UserUnion]
    }
    
    type BaseOrderResult {
        status: MutationStatus!
        order: BaseOrderUnion
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
    
    type AccountActionResult {
        status: MutationStatus!
        token: String
        user: User
    }
    
    type SaleResult {
        status: MutationStatus!
        sale: Sale
    }
    
    type UserResult {
        status: MutationStatus!
        user: User
    }
    
    type TagCategoryResult {
        status: MutationStatus!
        tag: Tag
        category: Category
    }
    
    type WorkerGroupResult {
        status: MutationStatus!
        group: Group
        worker: Worker
    }
    
    type GroupPermissionResult {
        status: MutationStatus!
        group: Group
        permission: Permission
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
        rooms: RoomsResult!
        familiar: [Category]!
        sales: [Sale]!
        bookedDates(dateStart: Date!, dateEnd: Date!): [Date]!
    }
    
    input DatesInput {
        dateStart: Date,
        dateEnd: Date
    }
    
    type Client {
        id: Int!
        firstName: String
        lastName: String
        email: String!
        dateOfBirth: Date
    }
    
    type User {
        id: Int!
        firstName: String
        lastName: String
        email: String!
        date_created: String!
        is_confirmed: String!
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
        client: ClientResult!
        purchases: PurchasesResult!
    }
    
    type ClientOrder {
        id: Int!
        price: Float!
        prepayment: Float!
        comment: String
        paid: Float!
        refunded: Float!
        leftToPay: Float!
        leftToRefund: Float!
        dateCreated: Datetime!
        dateFullPrepayment: Datetime
        dateFullPaid: Datetime
        dateFinished: Datetime
        dateCanceled: Datetime
        purchases: [Purchase]!
    }
    
    type Cart {
        id: Int!
        cartUuid: String!
        dateCreated: Datetime!
        price: Float!
        prepayment: Float!
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
        order: BaseOrderResult!
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
    
    type Permission {
        id: Int!
        name: String!
        code: String!
    }
    
    type Group {
        id: Int!
        name: String!
        permissions: PermissionsResult!
        users: UsersResult!
    }
    
    type Worker {
        id: Int!
        firstName: String
        lastName: String
        email: String!
        salary: Float!
        groups: GroupsResult!
    }
    
    type AuthTokens {
        access_token: String!
        refresh_token: String!
    }
"""
